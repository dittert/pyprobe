# coding=utf-8

import unittest
from os import path
from pyprobe.sensors.smart.sensor_smart import SmartSensor

__author__ = 'Dirk Dittert'

FAKE_UTIL = path.join(path.dirname(__file__), 'smartctl.py')


class SmartSensorDefinitionTest(unittest.TestCase):

    def test_missing_smartctl_should_return_none(self):
        sensor = SmartSensor()
        result = sensor.define({u'executable': u'afjalsfjalfjalsfjalf'})
        self.assertIsNone(result)