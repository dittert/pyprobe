# coding=utf-8
from os import path
import unittest

from integration.pegasus.test_helper import get_channel
from pyprobe import SensorError, SensorResult, LookupRaidStatusChannel
from pyprobe.sensors.appleraid.sensor_appleraid import AppleRaidSensor


__author__ = 'Dirk Dittert'

FAKE_UTIL = path.join(path.dirname(__file__), 'diskutil.py')
FAIL = path.join(path.dirname(path.dirname(__file__)), 'fail.py')


class AppleRaidSensorDefinitionTest(unittest.TestCase):

    def test_mountpoint_should_be_mandatory(self):
        subject = AppleRaidSensor()
        with self.assertRaises(ValueError):
            subject.execute('1234', '127.0.0.1', {}, {})

    def test_failure_during_execution_should_return_error(self):
        subject = AppleRaidSensor()
        result = subject.execute('1234', '127.0.0.1', {'mountpoint': '/Volumes/Space'}, {'executable': FAIL})

        self.assertIsInstance(result, SensorError)
        self.assertEqual(AppleRaidSensor.ERROR_CODE_EXECUTION, result.code)

    def test_valid_raid_should_return_correct_channel(self):
        subject = AppleRaidSensor()
        result = subject.execute('1234', '127.0.0.1', {'mountpoint': '/Volumes/Space'}, {'executable': FAKE_UTIL})

        self.assertIsInstance(result, SensorResult)
        self.assertEqual(LookupRaidStatusChannel.CODE_OK, get_channel(result, "Status").value)

    def test_degraded_raid_should_return_correct_channel(self):
        subject = AppleRaidSensor()
        result = subject.execute('1234', '127.0.0.1', {'mountpoint': '/Volumes/Degraded'}, {'executable': FAKE_UTIL})

        self.assertIsInstance(result, SensorResult)
        self.assertEqual(LookupRaidStatusChannel.CODE_DEGRADED, get_channel(result, "Status").value)
