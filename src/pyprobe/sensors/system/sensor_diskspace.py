# coding=utf-8
import psutil
from pyprobe.sensors import *

__author__ = 'Dirk Dittert'


class DiskSpaceSensor(BaseSensor):
    KIND = u'diskspace'

    def define(self, configuration):
        result = SensorDescription(u"Laufwerkskapazität", self.KIND)
        result.description = u"Monitort den freien Speicherplatz eines Laufwerks"
        group = GroupDescription(u"settings", u"Einstellungen")
        field_drive = FieldDescription(u"device", u"Laufwerk")
        field_drive.help = u"Geben Sie das Laufwerk an, dessen freier Speicherplatz überwacht werden soll (z.B. / " \
                           u"oder /mnt/drive. Sie können die gewünschten Grenzwerte in den Kanälen des Sensors" \
                           u"konfigurieren."
        field_drive.required = True
        group.fields.append(field_drive)
        result.groups.append(group)
        return result

    def execute(self, sensorid, host, parameters, configuration):
        if not "device" in parameters:
            raise ValueError("Parameter device is a mandatory parameter.")
        device = parameters["device"]
        usage = psutil.disk_usage(device)
        result = SensorResult(sensorid)
        free = max(100.0 - usage.percent, 0)
        channel = SensorChannel(u"Freier Platz", ModeType.FLOAT, ValueType.PERCENT, free)
        result.channel.append(channel)
        channel = SensorChannel(u"Freie Bytes", ModeType.INTEGER, ValueType.BYTES_DISK, usage.free)
        result.channel.append(channel)
        return result