# coding=utf-8
from os import path
import unittest

from pyprobe.sensors.appleraid.sensor_appleraid import AppleRaidSensor
from utils import Platform


__author__ = 'Dirk Dittert'

FAKE_UTIL = path.join(path.dirname(__file__), 'diskutil.py')


class AppleRaidSensorDefinitionTest(unittest.TestCase):

    def test_sensor_should_not_be_applicable_on_linux(self):
        with Platform("Linux"):
            subject = AppleRaidSensor()
            result = subject.define({'executable': FAKE_UTIL})
            self.assertIsNone(result)

    def test_sensor_should_be_applicable_on_os_x(self):
        with Platform("Darwin"):
            subject = AppleRaidSensor()
            result = subject.define({'executable': FAKE_UTIL})
            self.assertIsNotNone(result)