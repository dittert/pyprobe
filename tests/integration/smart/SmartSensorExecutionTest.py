# coding=utf-8

import unittest
from os import path
from integration.pegasus.test_helper import get_channel

from pyprobe import SensorError, SensorResult
from pyprobe.sensors.smart.definitions import ERROR_CODE_DRIVE_FAILING
from pyprobe.sensors.smart.sensor_smart import SmartSensor


__author__ = 'Dirk Dittert'

FAKE_UTIL = path.join(path.dirname(__file__), u'smartctl.py')
FAIL = path.join(path.dirname(path.dirname(__file__)), u'fail.py')


class SmartSensorExecutionTest(unittest.TestCase):

    def test_execution_failure_should_return_error(self):
        sensor = SmartSensor()
        result = sensor.execute(u'1234', u'127.0.0.1',
                                {u'device': u'/dev/disk1', u'strict': SmartSensor.FAILING_ONLY_ID},
                                {u'executable': FAIL})

        self.assertIsInstance(result, SensorError)
        self.assertEqual(SmartSensor.ERROR_CODE_EXECUTION, result.code)

    def test_smart_failure_should_return_error(self):
        sensor = SmartSensor()
        result = sensor.execute(u'1234', u'127.0.0.1',
                                {u'device': u'/dev/failed', u'strict': SmartSensor.FAILING_ONLY_ID},
                                {u'executable': FAKE_UTIL})

        self.assertIsInstance(result, SensorError)
        self.assertEqual(ERROR_CODE_DRIVE_FAILING, result.code)

    def test_failed_in_past_should_return_error(self):
        sensor = SmartSensor()
        result = sensor.execute(u'1234', u'127.0.0.1',
                                {u'device': u'/dev/failed', u'strict': SmartSensor.FAILING_ONLY_ID},
                                {u'executable': FAKE_UTIL})

        self.assertIsInstance(result, SensorError)
        self.assertEqual(ERROR_CODE_DRIVE_FAILING, result.code)

    def test_channels_should_be_returned(self):
        sensor = SmartSensor()
        result = sensor.execute(u'1234', u'127.0.0.1',
                                {u'device': u'/dev/disk1', u'strict': SmartSensor.FAILING_ONLY_ID},
                                {u'executable': FAKE_UTIL})

        self.assertIsInstance(result, SensorResult)

        actual_channel = {c.name for c in result.channel}
        expected_channel = {u'Seek Error Rate', u'Raw Read Error Rate', u'Spin Retry Count',
                            u'Reallocated Sector Count', u'Current Pending Sector', u'Temperatur',
                            u'Offline Uncorrectable'}
        self.assertEqual(expected_channel, actual_channel)

    def test_failing_only_should_have_no_limits(self):
        sensor = SmartSensor()
        result = sensor.execute(u'1234', u'127.0.0.1',
                                {u'device': u'/dev/disk1', u'strict': SmartSensor.FAILING_ONLY_ID},
                                {u'executable': FAKE_UTIL})

        self.assertIsInstance(result, SensorResult)

        expected_channel = {u'Seek Error Rate', u'Raw Read Error Rate', u'Spin Retry Count',
                            u'Reallocated Sector Count', u'Current Pending Sector', u'Temperatur',
                            u'Offline Uncorrectable'}
        for name in expected_channel:
            channel = get_channel(result, name)
            self.assertIsNone(channel.limit_max_error)
            self.assertFalse(channel.activate_limits)

        self.assertFalse(get_channel(result, u'Temperatur').activate_limits)
