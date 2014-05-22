# coding=utf-8
import unittest
from pyprobe.sensors.pegasus.sensor_phy_drive import PegasusPhysicalDriveSensor

__author__ = 'Dirk Dittert'


class PegasusDriveSensorTest(unittest.TestCase):

    def test_no_drive_should_throw(self):
        subject = PegasusPhysicalDriveSensor()
        with self.assertRaises(ValueError):
            subject.execute('1234', '127.0.0.1', {}, {})