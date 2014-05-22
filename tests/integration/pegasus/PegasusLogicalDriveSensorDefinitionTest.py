# coding=utf-8
from os import path
import unittest

from pyprobe.sensors.pegasus.sensor_log_drive import PegasusLogicalDriveSensor
from utils import Platform


__author__ = 'Dirk Dittert'

FAKE_UTIL = path.join(path.dirname(__file__), 'pegasus.py')


class PegasusLogicalDriveSensorExecutionTest(unittest.TestCase):

    def test_sensor_should_not_be_applicable_on_linux(self):
        with Platform("Linux"):
            sensor = PegasusLogicalDriveSensor()
            result = sensor.define({'executable': FAKE_UTIL})
            self.assertIsNone(result)

    def test_sensor_should_be_applicable_on_mac(self):
        with Platform("Darwin"):
            sensor = PegasusLogicalDriveSensor()
            result = sensor.define({'executable': FAKE_UTIL})
            self.assertIsNotNone(result)
