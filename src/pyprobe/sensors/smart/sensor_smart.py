# coding=utf-8
from collections import OrderedDict
import platform
import subprocess
from os import path

from pyprobe.sensors import *
from pyprobe.sensors.process_helper import get_outputs_of_process
from pyprobe.sensors.smart.smart_parser import SmartParser
from pyprobe.sensors.smart.smart_sensor_core import create_result_from_smart_channels
from pyprobe.utils import to_bytes


__author__ = 'Dirk Dittert'


class SmartSensor(BaseSensor):
    KIND = u"smartctl"

    ZERO_TOLERANCE_ID = u'1'
    FAILING_ONLY_ID = u'2'

    ERROR_CODE_EXECUTION = 0

    @staticmethod
    def _determine_executable(configuration):
        if platform.system() == "Darwin":
            return configuration.get("executable", "/usr/local/sbin/smartctl")
        elif platform.system() == "Linux":
            return configuration.get("executable", "/usr/sbin/smartctl")
        else:
            return configuration.get("executable", None)

    def define(self, configuration):
        executable = self._determine_executable(configuration)
        if not path.exists(executable):
            return None

        result = SensorDescription(u"S.M.A.R.T. Werte", self.KIND)
        result.description = u"Monitort die Werte einer Festplatte anhand der S.M.A.R.T. Daten."
        result.help = u"Dieser Sensor benötigt das Paket smartmontools."
        group = GroupDescription(u'settings', u'Einstellungen')
        field_device = FieldDescription(u"device", u"Device")
        field_device.required = True
        field_device.help = u"Das Laufwerk, dessen S.M.A.R.T. Werte überwacht werden sollen. Geben Sie hier " \
                            u"das zugehörige Device an (z.B. /dev/hda oder /dev/disk1)"
        group.fields.append(field_device)

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
        if u'device' not in parameters:
            raise ValueError("Parameter device is a mandatory parameter")
        device = parameters[u'device']
        if u'strict' not in parameters:
            raise ValueError('Parameter strict is a mandatory parameter')
        zero_tolerance = parameters['strict'] == self.ZERO_TOLERANCE_ID

        executable = self._determine_executable(configuration)

        command = u"LC_ALL=C {0} -a {1}".format(executable, device)
        proc = subprocess.Popen(to_bytes(command), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, out = get_outputs_of_process(proc)

        if proc.returncode != 0:
            message = u"{} returned with exit code {}.".format(executable, proc.returncode)
            return SensorError(sensorid, self.ERROR_CODE_EXECUTION, message, ErrorType.RESPONSE)

        smart_parser = SmartParser(out)

        # Check if any attributes are above zero (i.e. error)
        return create_result_from_smart_channels(sensorid, smart_parser, zero_tolerance)