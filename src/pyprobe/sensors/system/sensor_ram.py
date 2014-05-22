# coding=utf-8
import psutil
from pyprobe.sensors import *

__author__ = 'Dirk Dittert'


class RamUsageSensor(BaseSensor):
    KIND = u'ramusage'

    def define(self, configuration):
        result = SensorDescription(u"Speicherinfo", self.KIND)
        result.description = u"Monitort den Speicherverbrauch."
        return result

    def execute(self, sensorid, host, parameters, configuration):
        ram = psutil.virtual_memory()
        result = SensorResult(sensorid)
        free_percent = max(0, 100.0 - ram.percent)
        channel = SensorChannel(u"Verfügbarer Speicher in Prozent", ModeType.FLOAT, ValueType.PERCENT, free_percent)
        result.channel.append(channel)
        channel = SensorChannel(u"Verfügbarer Speicher", ModeType.INTEGER, ValueType.BYTES_MEMORY, ram.available)
        result.channel.append(channel)
        return result
