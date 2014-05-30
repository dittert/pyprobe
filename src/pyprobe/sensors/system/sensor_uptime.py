# coding=utf-8
from datetime import datetime

import psutil

from pyprobe.sensors import *


__author__ = 'Dirk Dittert'


class UptimeSensor(BaseSensor):
    KIND = u'uptime'

    def define(self, configuration):
        result = SensorDescription(u"Laufzeit", self.KIND)
        result.description = u"Monitort die Laufzeit eines Geräts."
        return result

    def execute(self, sensorid, host, parameters, configuration):
        uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
        result = SensorResult(sensorid)
        channel = SensorChannel(u"System-Laufzeit", ModeType.FLOAT, ValueType.TIME_SECONDS, uptime.total_seconds())
        result.channel.append(channel)
        return result