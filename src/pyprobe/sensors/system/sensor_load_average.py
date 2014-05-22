# coding=utf-8
import os

from pyprobe.sensors import *

__author__ = 'Dirk Dittert'


class CpuLoadAverageSensor(BaseSensor):
    KIND = u'cpuloadaverage'

    def define(self, configuration):
        result = SensorDescription(u"Durchschnittliche Last", self.KIND)
        result.description = u"Monitort die durchschnittliche Systemlast."
        return result

    def execute(self, sensorid, host, parameters, configuration):
        av1, av2, av3 = os.getloadavg()
        result = SensorResult(sensorid)
        channel = SensorChannel(u"1 Minute", ModeType.FLOAT, ValueType.CUSTOM, av1, u"")
        channel.decimal_mode = DecimalModeType.CUSTOM
        channel.decimal_digits = 2
        result.channel.append(channel)

        channel = SensorChannel(u"5 Minuten", ModeType.FLOAT, ValueType.CUSTOM, av2, u"")
        channel.decimal_mode = DecimalModeType.CUSTOM
        channel.decimal_digits = 2
        result.channel.append(channel)

        channel = SensorChannel(u"15 Minuten", ModeType.FLOAT, ValueType.CUSTOM, av3, u"")
        channel.decimal_mode = DecimalModeType.CUSTOM
        channel.decimal_digits = 2
        result.channel.append(channel)
        return result