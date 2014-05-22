# coding=utf-8
import psutil
from pyprobe.sensors import *

__author__ = 'Dirk Dittert'


class CpuPerCoreSensor(BaseSensor):
    KIND = u'cpupercore'

    def define(self, configuration):
        result = SensorDescription(u"Prozessorlast", self.KIND)
        result.description = u"Monitort die Prozessorlast pro Core."
        return result

    def execute(self, sensorid, host, parameters, configuration):
        usage_cores = psutil.cpu_percent(interval=None, percpu=True)
        usage_total = psutil.cpu_percent(interval=None, percpu=False)
        result = SensorResult(sensorid)
        channel = SensorChannel(u"Gesamt", ModeType.FLOAT, ValueType.PERCENT, usage_total)
        result.channel.append(channel)
        for idx, value in enumerate(usage_cores):
            name = u"Prozessor {}".format(idx + 1)
            channel = SensorChannel(name, ModeType.FLOAT, ValueType.CPU, value)
            result.channel.append(channel)
        return result