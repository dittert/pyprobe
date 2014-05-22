# coding=utf-8
from collections import OrderedDict
import subprocess
import platform

from pyprobe.sensors import *
from pyprobe.sensors.pegasus.helper import reformat_smart_values, determine_executable, determine_controllers
from pyprobe.sensors.process_helper import get_outputs_of_process
from pyprobe.sensors.smart.smart_parser import SmartParser
from pyprobe.sensors.smart.smart_sensor_core import create_result_from_smart_channels
from pyprobe.utils import to_bytes


__author__ = 'Dirk Dittert'


class PegasusPhysicalDriveSensor(BaseSensor):
    KIND = u'pegasusdrive'

    ZERO_TOLERANCE_ID = u'1'
    FAILING_ONLY_ID = u'2'

    ERROR_CODE_EXECUTION = 1
    ERROR_CODE_DRIVE_NOT_FOUND = 2
    ERROR_CODE_INCONSISTENT_OUTPUT = 3

    def define(self, configuration):
        if platform.system() != "Darwin":
            # sensor is only applicable on OS X systems.
            return None

        controllers = determine_controllers(configuration)
        if len(controllers) != 1:
            # no controllers available in system
            return None

        result = SensorDescription(u'Promise Pegasus Laufwerk', PegasusPhysicalDriveSensor.KIND)
        result.description = u"Monitort den Zustand eines Laufwerks eines Promise RAID-Laufwerks."

        group = GroupDescription(u"settings", u"Einstellungen")
        field_drive = FieldDescription(u"drive", u"Laufwerk")
        field_drive.minimum = 1
        field_drive.default = 1
        field_drive.maximum = 8
        field_drive.help = u"Geben Sie die Nummer des zu überwachenden Laufwerks an. Das erste Laufwerk hat die " \
                           u"Nummer 1."
        group.fields.append(field_drive)

        # setting whether strict monitoring or relaxed monitoring should be used.
        field_strict = FieldDescription(u'strict', u'Modus', InputTypes.RADIO)
        field_strict.help = u'Laufwerke können als fehlerhaft betrachtet werden, wenn eines der überwachten Attribute' \
                            u'einen Wert > 0 annimmt oder wenn ihr S.M.A.R.T. Status als fehlerhaft markiert wird. ' \
                            u'Manche Festplatten (z.B. Hitachi) liefern wechselnde Werte, so dass hier nur ' \
                            u'als fehlerhafte markierte Attribute beachtet werden sollten.'
        field_strict.options = OrderedDict([
            (self.ZERO_TOLERANCE_ID, u'Attribute mit Werten > 0 als Fehler betrachten'),
            (self.FAILING_ONLY_ID, u'Nur fehlerhafte Attribute als Fehler betrachten')
        ])
        field_strict.default = self.FAILING_ONLY_ID
        group.fields.append(field_strict)
        result.groups.append(group)
        return result

    def execute(self, sensorid, host, parameters, configuration):
        if 'drive' not in parameters:
            raise ValueError("Parameter drive is a mandatory parameter")
        drive = int(parameters['drive'])
        executable = determine_executable(configuration)
        zero_tolerance = parameters['strict'] == self.ZERO_TOLERANCE_ID

        command = u"LC_ALL=C {0} -C smart -a list -p {1} -v".format(executable, drive)
        proc = subprocess.Popen(to_bytes(command), shell=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, out = get_outputs_of_process(proc)

        if out == u"Error (0x4020): physical drive not found\n" and proc.returncode == 32:
            message = u"Drive {0} not found.".format(drive)
            return SensorError(sensorid, self.ERROR_CODE_DRIVE_NOT_FOUND, message, ErrorType.DATA)
        elif proc.returncode != 0:
            message = u"{} returned with exit code {}.".format(executable, proc.returncode)
            return SensorError(sensorid, self.ERROR_CODE_EXECUTION, message, ErrorType.RESPONSE)

        attribute_section = reformat_smart_values(out)
        if attribute_section is None:
            message = u"Unexpected S.M.A.R.T. output. Check log files."
            return SensorError(sensorid, self.ERROR_CODE_INCONSISTENT_OUTPUT, message, ErrorType.DATA)
        smart_parser = SmartParser(attribute_section)

        # Check if any attributes are above zero (i.e. error)
        return create_result_from_smart_channels(sensorid, smart_parser, zero_tolerance)
