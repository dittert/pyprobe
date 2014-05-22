# coding=utf-8
import psutil
from pyprobe.sensors import *

__author__ = 'Dirk Dittert'


class DiskIOSensor(BaseSensor):
    KIND = u'diskio'

    ERROR_INVALID_DEVICE = 0

    def define(self, configuration):
        result = SensorDescription(u"IO Last", self.KIND)
        result.description = u"Monitort die IO-Auslasung einer Festplatte."
        group = GroupDescription(u"settings", u"Einstellungen")
        field_drive = FieldDescription(u"device", u"Laufwerk")
        field_drive.help = u"Geben Sie das Laufwerk an, dessen IO-Auslastung überwacht werden soll (z.B. /dev/disk0 " \
                           u"oder /dev/hda. Es können nur physikalische Laufwerke angegeben werden, keine " \
                           u"Software-RAIDLaufwerke oder Devicemapper Laufwerke."
        field_drive.required = True
        group.fields.append(field_drive)
        result.groups.append(group)
        return result

    def execute(self, sensorid, host, parameters, configuration):
        if not u'device' in parameters:
            raise ValueError("Parameter device is a required parameter.")
        device = parameters[u'device']

        counters = psutil.disk_io_counters(perdisk=True)
        devices = [u"/dev/{}".format(d) for d in counters.keys()]
        if not device in devices:
            message = u"Unbekanntes Gerät {}. Mögliche Geräte sind: {}".format(device, ", ".join(devices))
            return SensorError(sensorid, self.ERROR_INVALID_DEVICE, message)

        data = next(d[1] for d in counters.items() if u"/dev/{}".format(d[0]) == device)
        result = SensorResult(sensorid)
        channel = SensorChannel(u"Summe Byte", ModeType.COUNTER, u"SpeedDisk",
                                data.read_bytes + data.write_bytes)
        channel.speed_size = SizeUnitType.KILO_BYTE
        channel.volume_size = SizeUnitType.MEGA_BYTE
        result.channel.append(channel)
        channel = SensorChannel(u"Byte gelesen", ModeType.COUNTER, u"SpeedDisk",
                                data.read_bytes)
        channel.speed_size = SizeUnitType.KILO_BYTE
        channel.volume_size = SizeUnitType.MEGA_BYTE
        result.channel.append(channel)
        channel = SensorChannel(u"Byte geschrieben", ModeType.COUNTER, u"SpeedDisk",
                                data.write_bytes)
        channel.speed_size = SizeUnitType.KILO_BYTE
        channel.volume_size = SizeUnitType.MEGA_BYTE
        result.channel.append(channel)
        channel = SensorChannel(u"EA Operationen", ModeType.COUNTER, ValueType.COUNT,
                                data.read_count + data.write_count)
        result.channel.append(channel)
        return result

