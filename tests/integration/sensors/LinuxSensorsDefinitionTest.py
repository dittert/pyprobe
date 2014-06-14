# coding=utf-8
from os import path
import unittest
from pyprobe.sensors.sensors.sensor_coretemp import LinuxCoreTempSensor
from utils import Platform

__author__ = 'Dirk Dittert'

FAKE_UTIL = path.join(path.dirname(__file__), 'sensors.py')
NO_CORETEMP_UTIL = path.join(path.dirname(__file__), 'no_coretemp.py')


class LinuxSensorsDefinitionTest(unittest.TestCase):

    def test_sensor_should_not_be_available_on_darwin(self):
        with Platform("Darwin"):
            sensor = LinuxCoreTempSensor()
            subject = sensor.define({'executable': FAKE_UTIL})

            self.assertIsNone(subject)

    def test_sensor_should_be_available_on_linux(self):
        with Platform("Linux"):
            sensor = LinuxCoreTempSensor()
            subject = sensor.define({'executable': FAKE_UTIL})

            self.assertIsNotNone(subject)