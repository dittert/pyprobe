# coding=utf-8

import unittest
# noinspection PyPackageRequirements
from mock import MagicMock
import psutil
from integration.pegasus.test_helper import get_channel
from pyprobe import SensorError
from pyprobe.sensors.system.sensor_diskio import DiskIOSensor


class Container(object):
    def __init__(self):
        self.read_count = 120L
        self.write_count = 240L
        self.read_bytes = 150L
        self.write_bytes = 200L

IOVALUES = {
    u'disk0': Container()}

__author__ = 'Dirk Dittert'


class DiskIOSensorTest(unittest.TestCase):

    def test_missing_device_should_raise(self):
        with self.assertRaises(ValueError):
            subject = DiskIOSensor()
            subject.execute(u'1234', u'127.0.0.1', {}, {})

    def test_invalid_device_should_return_error(self):
        with IOCounters(IOVALUES):
            subject = DiskIOSensor()
            result = subject.execute(u'1234', u'127.0.0.1', {u'device': u'/dev/disk1'}, {})
            self.assertIsInstance(result, SensorError)
            self.assertEqual(u'Unbekanntes Gerät /dev/disk1. Mögliche Geräte sind: /dev/disk0', result.message)

    def test_valid_device_should_return_values(self):
        with IOCounters(IOVALUES):
            subject = DiskIOSensor()
            result = subject.execute(u'1234', u'127.0.0.1', {u'device': u'/dev/disk0'}, {})
            self.assertEqual(350, get_channel(result, u"Summe Byte").value)
            self.assertEqual(150, get_channel(result, u"Byte gelesen").value)
            self.assertEqual(200, get_channel(result, u"Byte geschrieben").value)
            self.assertEqual(360, get_channel(result, u"EA Operationen").value)


class IOCounters(object):
    def __init__(self, values):
        self._oldptr = None
        self._values = values

    def __enter__(self):
        self._oldptr = psutil.disk_io_counters
        psutil.disk_io_counters = MagicMock(return_value=self._values)

    # noinspection PyUnusedLocal
    def __exit__(self, exc_type, exc_val, exc_tb):
        psutil.disk_io_counters = self._oldptr