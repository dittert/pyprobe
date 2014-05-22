# coding=utf-8
from os import path
import unittest
from pyprobe import SensorError, LookupRaidStatusChannel
from pyprobe.results import SensorResult
from pyprobe.sensors.pegasus.sensor_log_drive import PegasusLogicalDriveSensor
from integration.pegasus.test_helper import get_channel

__author__ = 'Dirk Dittert'

FAKE_UTIL = path.join(path.dirname(__file__), 'pegasus.py')
DEAD_DRIVE = path.join(path.dirname(__file__), 'dead_logical_drive.py')
UNSYNCED_DRIVE = path.join(path.dirname(__file__), 'unsynced_logical_drive.py')


class PegasusLogicalDriveSensorExecutionTest(unittest.TestCase):

    def test_no_wwn_should_raise(self):
        subject = PegasusLogicalDriveSensor()
        with self.assertRaises(ValueError):
            subject.execute('1234', '127.0.0.1', {}, {})

    def test_invalid_wwn_should_return_error(self):
        subject = PegasusLogicalDriveSensor()
        result = subject.execute('1234', '127.0.0.1', {'wwn': '1234'}, {'executable': FAKE_UTIL})

        self.assertIsInstance(result, SensorError)
        self.assertEqual("Es wurde kein Array mit WWN '1234'  gefunden.", result.message)

    def test_dead_drive_should_set_state_to_degraded(self):
        subject = PegasusLogicalDriveSensor()
        result = subject.execute('1234', '127.0.0.1', {'wwn': '1111-0001-88b8-9999'}, {'executable': DEAD_DRIVE})

        self.assertIsInstance(result, SensorResult)
        self.assertEqual(LookupRaidStatusChannel.CODE_DEGRADED, get_channel(result, "Status").value)

    def test_unsynced_drive_should_return_degraded_state(self):
        subject = PegasusLogicalDriveSensor()
        result = subject.execute('1234', '127.0.0.1', {'wwn': '1111-0001-88b8-9999'}, {'executable': UNSYNCED_DRIVE})

        self.assertIsInstance(result, SensorResult)
        self.assertEqual(LookupRaidStatusChannel.CODE_REBUILDING, get_channel(result, "Status").value)

    def test_valid_drive_should_return_result(self):
        subject = PegasusLogicalDriveSensor()
        result = subject.execute('1234', '127.0.0.1', {'wwn': '1111-0001-88b8-9999'}, {'executable': FAKE_UTIL})

        self.assertIsInstance(result, SensorResult)
        self.assertEqual(LookupRaidStatusChannel.CODE_OK, get_channel(result, "Status").value)
