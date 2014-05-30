#!/usr/bin/env python2.7
# coding=utf-8
from collections import OrderedDict
from optparse import OptionParser
from os import path
import sys
import platform
import json
import traceback
import uuid
import datetime
import syslog

import requests
from requests.exceptions import ConnectionError, Timeout

import pyprobe
from pyprobe.sensors.appleraid.sensor_appleraid import AppleRaidSensor
from pyprobe.sensors.system.sensor_diskio import DiskIOSensor
from pyprobe.sensors.system.sensor_diskspace import DiskSpaceSensor
from pyprobe.sensors.system.sensor_load_average import CpuLoadAverageSensor
from pyprobe.sensors.system.sensor_cpu_per_core import CpuPerCoreSensor
from pyprobe.sensors.pegasus import PegasusPhysicalDriveSensor
from pyprobe.sensors.pegasus.sensor_enclosure import PegasusEnclosureSensor
from pyprobe.sensors.pegasus.sensor_log_drive import PegasusLogicalDriveSensor
from pyprobe.sensors.ping.sensor_ping import PingSensor
from pyprobe.configuration import InvalidConfig, ConfigHandler
from pyprobe.sensors.smart.sensor_smart import SmartSensor
from pyprobe.sensors.system.sensor_ram import RamUsageSensor
from pyprobe.sensors.system.sensor_swap import SwapUsageSensor
from pyprobe.sensors.system.sensor_uptime import UptimeSensor
from pyprobe.utils import to_utf8


_sensors = OrderedDict()
""":type: dict[unicode, pyprobe.configuration.BaseSensor]"""

_handler = None
""":type: ConfigHandler """

_config = None
""":type: pyprobe.ProbeConfiguration"""

_config_path = None
""":type: unicode"""

_state_path = None
""":type: unicode"""

_verbose = False


def _init_state_path(cmd_options):
    global _state_path

    if platform.system() == "Darwin":
        default_location = "/Library/Application Support/de.tfobjects.pyprobe.state"
    elif platform.system() == "Linux":
        default_location = "/var/cache/pyprobe/pyprtg.state"
    else:
        default_location = None

    if cmd_options.state_file is None and default_location is None:
        raise InvalidConfig("No place to store probe state information. Check documentation.")

    if cmd_options.state_file is not None:
        _state_path = path.abspath(cmd_options.state_file)
    else:
        _state_path = default_location


def _init_config(cmd_options):
    global _config
    global _handler
    global _config_path

    if platform.system() == "Darwin":
        default_location = u"/Library/Preferences/de.tfobjects.pyprobe.config"
    elif platform.system() == "Linux":
        default_location = u"/etc/pyprobe"
    else:
        default_location = None

    # No config file and no file at default location...
    if cmd_options.config_file is None and default_location is None:
        raise InvalidConfig("No config file")

    if cmd_options.config_file is not None:
        _config_path = path.abspath(cmd_options.config_file)
    else:
        _config_path = default_location

    if not path.exists(_config_path) and not path.isfile(_config_path):
        message = "Config file not found at {}. Exiting...\n".format(_config_path)
        syslog.syslog(syslog.LOG_ERR, message)
        sys.stderr.write(message + "\n")
        exit(-1)

    _handler = ConfigHandler(_config_path, _state_path)
    _config = _handler.config()


def _init_sensors():
    _sensors[PingSensor.KIND] = PingSensor()

    _sensors[CpuPerCoreSensor.KIND] = CpuPerCoreSensor()
    _sensors[CpuLoadAverageSensor.KIND] = CpuLoadAverageSensor()
    _sensors[RamUsageSensor.KIND] = RamUsageSensor()
    _sensors[SwapUsageSensor.KIND] = SwapUsageSensor()

    _sensors[DiskSpaceSensor.KIND] = DiskSpaceSensor()
    _sensors[DiskIOSensor.KIND] = DiskIOSensor()
    _sensors[UptimeSensor.KIND] = UptimeSensor()

    _sensors[SmartSensor.KIND] = SmartSensor()
    _sensors[PegasusLogicalDriveSensor.KIND] = PegasusLogicalDriveSensor()
    _sensors[PegasusPhysicalDriveSensor.KIND] = PegasusPhysicalDriveSensor()
    _sensors[PegasusEnclosureSensor.KIND] = PegasusEnclosureSensor()
    _sensors[AppleRaidSensor.KIND] = AppleRaidSensor()


class ProbeException(Exception):
    pass


class AccessDeniedException(ProbeException):
    """
    Exception that occurs if the local probe is denied access by the core server (i.e. it was not authorized yet
    or it was banned on the server).
    """
    pass


def _check_access_to_server(r):
    if r.status_code == 401 and r.text == "Access denied by GID filter!":
        raise AccessDeniedException()
    if r.status_code != 200:
        raise ProbeException(r.text)


def _register_probe():
    # ensure that a GID is set for this probe.
    handler = _handler.state_handler()
    if handler.gid is None:
        _create_new_gid()

    # This is not done in a list comprehension because exceptions thrown by a sensor should not disturb the
    # operation of the probe.
    sensors = []
    for s in _sensors.values():
        # noinspection PyBroadException
        try:
            definition = s.define(_handler.config_for_sensor(s.KIND))
            if definition is not None:
                sensors.append(definition)
        except Exception:
            message = "Error calling define() for sensor kind {}. Sensor was ignored.".format(s.KIND)
            sys.stderr.write(message + "\n")
            trace = traceback.format_exc()
            syslog.syslog(syslog.LOG_ERR, message)
            syslog.syslog(syslog.LOG_ERR, trace)
            sys.stderr.write(trace)

    encoded_sensor_description = json.dumps(sensors, cls=pyprobe.DescriptionJSONEncoder, ensure_ascii=False)
    payload = {
        'gid': handler.gid,
        'key': _config.key.encrypted,
        'protocol': '1',

        'name': _config.probe_name,
        'version': '1',
        'baseinterval': _config.base_interval,
        'sensors': to_utf8(encoded_sensor_description),
    }
    for i in xrange(3):
        try:
            res = requests.post(_config.prtg_url + '/probe/announce', data=payload, verify=False, timeout=10.0)
            _check_access_to_server(res)
            break
        except ConnectionError as ex:
            message = "Could not register probe with server."
            syslog.syslog(syslog.LOG_ERR, message)
            sys.stderr.write(message + '\n')
            raise ProbeException(ex.message)
        except Timeout:
            pass


def _query_tasks():
    """
    :rtype: list[QueryTask]
    """
    getpayload = {
        'gid': _handler.state_handler().gid,
        'key': _config.key,
        'protocol': '1',
    }
    for i in xrange(3):
        try:
            r = requests.get(_config.prtg_url + '/probe/tasks', params=getpayload, verify=False, timeout=10.0)
            _check_access_to_server(r)
            p = pyprobe.TaskParser(r.status_code, r.text)
            return p.tasks()
        except ConnectionError:
            message = "Failed to retrieve tasks from server."
            sys.stderr.write(message + "\n")
            syslog.syslog(syslog.LOG_ERR, message)
            trace = traceback.format_exc()
            syslog.syslog(syslog.LOG_ERR, trace)
            sys.stderr.write(trace)
            return []
        except Timeout:
            pass
    else:
        return []


def _publish_results(resultlist):
    """
    :type resultlist: list
    """
    if resultlist is None or len(resultlist) == 0:
        return

    encoded_data = json.dumps(resultlist, cls=pyprobe.DescriptionJSONEncoder, ensure_ascii=False)
    payload = {
        'gid': _handler.state_handler().gid,
        'key': _config.key.encrypted,
        'protocol': '1',

        'data': to_utf8(encoded_data),
    }

    if _verbose:
        now = datetime.datetime.now()
        print(now)
        print encoded_data
        print

    for i in xrange(3):
        try:
            res = requests.post(_config.prtg_url + '/probe/data', data=payload, verify=False, timeout=30.0)
            _check_access_to_server(res)
            message = "Published {} results to PRTG.".format(len(resultlist))
            syslog.syslog(syslog.LOG_DEBUG, message)
            if _verbose:
                sys.stderr.write(message + "\n")
            break
        except ConnectionError as ex:
            raise ProbeException(ex.message)
        except Timeout:
            pass
    else:
        # There is no use in keeping this info around as the sensor results are not time stamped. New results will be
        # generated by the sensors soon, so we just throw them out...
        message = "{} results were lost because the server could not be reached.".format(len(resultlist))
        syslog.syslog(syslog.LOG_ERR, message)
        sys.stderr.write(message + "\n")


def _create_new_gid():
    new_uuid = str(uuid.uuid4())
    handler = _handler.state_handler()
    handler.gid = new_uuid
    handler.update_or_create()
    return new_uuid


def _handle_command_line_parameters(cmd_options):
    if cmd_options.verbose:
        global _verbose
        _verbose = True

    if cmd_options.info:
        print("pyProbe -- A Mini Probe for PRTG written in Python.")
        print
        print("This probe is named '{}' and will "
              "check every {} seconds for new tasks.".format(_config.probe_name, _config.base_interval))
        print("PRTG url:   " + _config.prtg_url)
        print("Probe name: " + _config.probe_name)

        gid = _handler.state_handler().gid
        if gid is None:
            print("GID:        Probe was not registered with server. It will be assigned on first\n"
                  "            contact. You can use --reset to manually force to set a GID.")
        else:
            print("GID:        " + gid)
        print
        print("Configuration files:")
        print("Config:     " + _config_path)
        print("State:      " + _state_path)
        print
        print("Available sensors:")
        for s in _sensors.values():
            config = _handler.config_for_sensor(s.KIND)
            info = s.define(config)
            if info is not None:
                if info.description is None:
                    print(" - " + info.name)
                else:
                    print(" - " + info.name + ": " + info.description)
        sys.exit(0)

    if cmd_options.reset:
        new_uuid = _create_new_gid()
        print("Local configuration was reset. GID is now {0}".format(new_uuid))
        sys.exit(0)


def main():
    syslog.syslog(u'pyprobe starting...')
    try:
        parser = OptionParser(description='A Mini Probe implementation for PRTG.', prog='pyprobe')
        parser.add_option("-i", "--info", dest="info", action="store_true",
                          help="show probe information and exit")
        parser.add_option("-v", "--verbose", dest="verbose", action="store_true", help="create verbose output")
        parser.add_option("--reset", dest="reset", action="store_true",
                          help="Resets the local state of the probe. This causes the probe to reregister when it is "
                               "started up again. PRTG will consider it as a new probe, even if the name remains "
                               "unchanged.")
        parser.add_option("--config", dest="config_file", help="read configuration from FILE", metavar="FILE")
        parser.add_option("--state", dest="state_file", help="read the probe internal state from file FILE",
                          metavar="FILE")
        (options, args) = parser.parse_args()

        _init_state_path(options)
        _init_config(options)
        _init_sensors()
        _handle_command_line_parameters(options)
        try:
            _register_probe()
        except AccessDeniedException:
            message = "Probe was not authorized or banned on core server. Unable to continue"
            syslog.syslog(syslog.LOG_ERR, message)
            print(message)
            sys.exit(1)

        while True:
            if _verbose:
                print("starting sensor check")
            iteration = pyprobe.Iteration(_config.base_interval)
            iteration.start_timer()
            try:
                tasks = _query_tasks()
                results = []
                for task in tasks:
                    sensor = _sensors[task.kind]
                    if sensor is None:
                        raise ValueError("Unknown sensor type {0}".format(task.kind))
                    config_for_sensor = _handler.config_for_sensor(task.kind)
                    # noinspection PyBroadException
                    try:
                        sensorresult = sensor.execute(task.sensorid, task.host, task.parameters, config_for_sensor)
                        if sensorresult is not None:
                            results.append(sensorresult)
                    except Exception as e:
                        trace = traceback.format_exc()
                        syslog.syslog(syslog.LOG_ERR, trace)
                        if _verbose:
                            sys.stderr.write(trace)
                        from pyprobe.results import SensorError, ErrorType
                        results.append(SensorError(task.sensorid, 0, e.message, ErrorType.EXCEPTION))
                _publish_results(results)

            except AccessDeniedException:
                message = "Probe was not authorized or banned on core server. Unable to continue"
                syslog.syslog(syslog.LOG_ERR, message)
                print(message)
                sys.exit(1)
            except ProbeException:
                trace = traceback.format_exc()
                syslog.syslog(syslog.LOG_ERR, trace)
                sys.stderr.write(trace)
            iteration.stop_timer()
            iteration.wait_until_next_iteration()

    except KeyboardInterrupt:
        sys.exit()

if __name__ == "__main__":
    main()
