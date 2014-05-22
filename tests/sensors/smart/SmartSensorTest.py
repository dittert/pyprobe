# coding=utf-8

import unittest
from pyprobe.sensors.smart.sensor_smart import SmartSensor

__author__ = 'Dirk Dittert'

class SmartSensorTest(unittest.TestCase):

    def test_missing_device_parameter_should_raise(self):
        with self.assertRaises(ValueError):
            sensor = SmartSensor()
            sensor.execute('1234', '127.0.0.1', {}, {})