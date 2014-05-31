# coding=utf-8

from pyprobe.sensors import *


__author__ = 'Dirk Dittert'


class ProbeInfoSensor(BaseSensor):
    KIND = u'probeinfo'

    def __init__(self, info):
        super(ProbeInfoSensor, self).__init__()
        self.info = info
        """ :type: ProbeInfo """

    def define(self, configuration):
        result = SensorDescription(u"Probeinformationen", self.KIND)
        result.description = u"Liefert Informationen über die Probe."
        result.help = u"Informationen über Anzahl der übertragenen Sensorergebnisse und der dafür angefallenen " \
                      u"Datenmenge (genähert)"
        return result

    def execute(self, sensorid, host, parameters, configuration):
        result = SensorResult(sensorid)
        channel = SensorChannel(u"Sensorwerte", ModeType.COUNTER, ValueType.COUNT, self.info.count())
        result.channel.append(channel)

        channel = SensorChannel(u"Datenvolumen", ModeType.COUNTER, ValueType.SPEED_DISK, self.info.bytes())
        result.channel.append(channel)
        return result