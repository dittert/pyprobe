# coding=utf-8
import platform
import subprocess

from pyprobe.sensors import *
from pyprobe.sensors.pegasus.enclosure import EnclosureParser
from pyprobe.sensors.pegasus.helper import determine_executable, determine_controllers
from pyprobe.sensors.process_helper import get_outputs_of_process
from pyprobe.utils import to_bytes


__author__ = 'Dirk Dittert'


class PegasusEnclosureSensor(BaseSensor):
    KIND = u"pegasusenclosure"

    ERROR_CODE_EXECUTION_ERROR = 1
    ERROR_CODE_FAN_ERROR = 2
    ERROR_CODE_TEMPERATURE_ERROR = 3

    def define(self, configuration):
        if platform.system() != "Darwin":
            # sensor is only applicable on OS X systems.
            return None

        controllers = determine_controllers(configuration)
        if len(controllers) != 1:
            # no controllers available in system
            return None

        result = SensorDescription(u"Promise Pegasus Enclosure", self.KIND)
        result.description = u"Monitort ein Promise Pegasus RAID-Gehäuse."
        return result

    def execute(self, sensorid, host, parameters, configuration):
        executable = determine_executable(configuration)

        command = u"LC_ALL=C {0} -C enclosure -e 1 -v".format(executable)
        proc = subprocess.Popen(to_bytes(command), shell=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, out = get_outputs_of_process(proc)

        if proc.returncode != 0:
            message = u"Ausführung von {} ist mit Fehlercode {} gescheitert.".format(executable, proc.returncode)
            return SensorError(sensorid, self.ERROR_CODE_EXECUTION_ERROR, message, ErrorType.RESPONSE)

        parser = EnclosureParser(out)

        # Check fan speed
        fan = parser.fan()
        if not fan.ok():
            if fan.speed is not None:
                message = u"Lüfterdrehzahl {} RPM ist unterhalb " \
                          u"der Minimaldrehzahl von {} RPM.".format(fan.speed, fan.threshold)
            else:
                message = u"Lüfterdrehzahl konnte nicht ermittelt werden. Möglicher Lüfterdefekt!"
            return SensorError(sensorid, self.ERROR_CODE_FAN_ERROR, message, ErrorType.DATA)

        # Check temperature thresholds
        for sensor in parser.temperatures():
            if not sensor.ok():
                message = u"Temperatur {}°C von Sensor '{}' " \
                          u"liegt über dem Grenzwert {}°C " \
                          u"(Sensorstatus: {}).".format(sensor.value, sensor.name, sensor.threshold, sensor.status)
                return SensorError(sensorid, self.ERROR_CODE_TEMPERATURE_ERROR, message, ErrorType.DATA)

        result = SensorResult(sensorid)
        for sensor in parser.temperatures():
            name = u"{} Temperatur".format(sensor.name)
            channel = SensorChannel(name, ModeType.INTEGER, ValueType.TEMPERATURE, sensor.value)
            result.channel.append(channel)
        channel = SensorChannel(u"Lüfterdrehzahl", ModeType.INTEGER, ValueType.CUSTOM, fan.speed, u"RPM")
        result.channel.append(channel)
        return result