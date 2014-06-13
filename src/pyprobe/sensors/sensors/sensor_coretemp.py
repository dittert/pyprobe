# coding=utf-8
import platform
from pyprobe.sensors import BaseSensor

__author__ = 'Dirk Dittert'


class CoreTempSensor(BaseSensor):
    KIND = u'sensorscoretemp'

    def define(self, configuration):
        if platform.system() != "Linux":
            return None

    def execute(self, sensorid, host, parameters, configuration):
        return None