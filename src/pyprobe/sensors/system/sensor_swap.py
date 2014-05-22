# coding=utf-8
from pyprobe.sensors import *
import psutil

__author__ = 'Dirk Dittert'


class SwapUsageSensor(BaseSensor):
    KIND = u'swapusage'

    def define(self, configuration):
        result = SensorDescription(u"Auslagerungsdatei", self.KIND)
        result.description = u"Monitort die Verwendung der Auslagerungsdatei."
        return result

    def execute(self, sensorid, host, parameters, configuration):
        mem = psutil.swap_memory()
        result = SensorResult(sensorid)
        channel = SensorChannel(u"Belegt %", ModeType.FLOAT, ValueType.PERCENT, mem.percent)
        channel.limit_max_error = 90.0
        channel.limit_max_warning = 60.0
        result.channel.append(channel)

        channel = SensorChannel(u'Frei', ModeType.INTEGER, ValueType.BYTES_MEMORY, mem.free)
        result.channel.append(channel)
        channel.show_chart = False
        channel = SensorChannel(u'Belegt', ModeType.INTEGER, ValueType.BYTES_MEMORY, mem.used)
        channel.show_chart = False
        result.channel.append(channel)

        return result


