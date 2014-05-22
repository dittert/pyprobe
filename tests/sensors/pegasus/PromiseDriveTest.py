# coding=utf-8
import unittest
from pyprobe.sensors.pegasus.drives import PromiseDrive

__author__ = 'Dirk Dittert'


class PromiseDriveTest(unittest.TestCase):

    def test_failed_should_be_detected(self):
        drive = PromiseDrive()
        drive.status = "Failure"

        self.assertTrue(drive.failed())

    def test_warning_should_be_detected(self):
        drive = PromiseDrive()
        drive.model = "Hitachi HDS72302"
        drive.capacity = "2TB"
        drive.location = "Encl1 Slot1"
        drive.errors = 1
        drive.non_rw_errors = 1
        drive.read_errors = 1
        drive.write_errors = 1
        drive.status = PromiseDrive.STATUS_OK

        self.assertTrue(drive.warning())

    def test_successful_should_be_detected(self):
        drive = PromiseDrive()
        drive.status = PromiseDrive.STATUS_OK

        self.assertFalse(drive.failed())

    def test_str_of_ok_drive(self):
        drive = PromiseDrive()
        drive.model = "Hitachi HDS72302"
        drive.capacity = "2TB"
        drive.location = "Encl1 Slot1"
        drive.errors = 0
        drive.non_rw_errors = 0
        drive.read_errors = 0
        drive.write_errors = 0
        drive.status = PromiseDrive.STATUS_OK

        self.assertEqual("Drive Hitachi HDS72302 2TB in Encl1 Slot1", str(drive))

    def test_str_of_failed_drive(self):
        drive = PromiseDrive()
        drive.model = "Hitachi HDS72302"
        drive.capacity = "2TB"
        drive.location = "Encl1 Slot1"
        drive.errors = 0
        drive.non_rw_errors = 0
        drive.read_errors = 0
        drive.write_errors = 0
        drive.status = "FAILED"

        self.assertEqual("Failed Drive Hitachi HDS72302 2TB in Encl1 Slot1", str(drive))