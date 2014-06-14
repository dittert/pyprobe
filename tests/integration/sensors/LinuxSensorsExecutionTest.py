# coding=utf-8
from os import path
import unittest
from pyprobe import SensorError
from pyprobe.sensors.sensors.sensor_coretemp import LinuxCoreTempSensor
from utils import Platform

__author__ = 'Dirk Dittert'

FAKE_UTIL = path.join(path.dirname(__file__), 'sensors.py')
NO_CORETEMP_UTIL = path.join(path.dirname(__file__), 'no_coretemp.py')

ID = '1234'
LOCALHOST = '127.0.0.1'


class LinuxSensorsExecutionTest(unittest.TestCase):

    def test_no_sensors_should_return_error(self):
        with Platform("Linux"):
            subject = LinuxCoreTempSensor()
            params = {u'cpus': u'alle'}
            result = subject.execute(ID, LOCALHOST, params, {'executable': NO_CORETEMP_UTIL})

            self.assertIsInstance(result, SensorError)
            self.assertEqual(LinuxCoreTempSensor.ERROR_CODE_NO_CPUS, result.code)

    def test_channel_names_should_be_correct(self):
        with Platform("Linux"):
            subject = LinuxCoreTempSensor()
            params = {u'cpus': u'alle'}
            result = subject.execute(ID, LOCALHOST, params, {'executable': FAKE_UTIL})

            actual_channels = [c.name for c in result.channel]
            self.assertEqual([u'CPU 1-1', u'CPU 1-2', u'CPU 1-3', u'CPU 1-4',
                              u'CPU 2-1', u'CPU 2-2', u'CPU 2-3', u'CPU 2-4'], actual_channels)

    def test_channel_values_should_be_correct(self):
        with Platform("Linux"):
            subject = LinuxCoreTempSensor()
            params = {u'cpus': u'alle'}
            result = subject.execute(ID, LOCALHOST, params, {'executable': FAKE_UTIL})

            actual_values = [c.value for c in result.channel]
            self.assertEqual([43.0, 44.0, 45.0, 46.0, 47.0, 48.0, 49.0, 50.0], actual_values)

    def test_channel_names_should_be_correct_for_one_cpu(self):
        with Platform("Linux"):
            subject = LinuxCoreTempSensor()
            params = {u'cpus': u'coretemp-isa-0001'}
            result = subject.execute(ID, LOCALHOST, params, {'executable': FAKE_UTIL})

            actual_names = [c.name for c in result.channel]
            self.assertEqual([u'CPU 2-1', u'CPU 2-2', u'CPU 2-3', u'CPU 2-4'], actual_names)

    def test_channel_value_should_be_correct_for_one_cpu(self):
        with Platform("Linux"):
            subject = LinuxCoreTempSensor()
            params = {u'cpus': u'coretemp-isa-0001'}
            result = subject.execute(ID, LOCALHOST, params, {'executable': FAKE_UTIL})

            actual_values = [c.value for c in result.channel]
            self.assertEqual([47.0, 48.0, 49.0, 50.0], actual_values)
