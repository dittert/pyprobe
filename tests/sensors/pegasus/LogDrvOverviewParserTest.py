# coding=utf-8
import unittest
from pyprobe.sensors.pegasus.drives import LogDrvOverviewParser

__author__ = 'Dirk Dittert'

SINGLE_DRIVE = """\

-------------------------------------------------------------------------------
LdId: 0
ArrayId: 0                             SYNCed: Yes
OperationalStatus: OK
Alias:
SerialNo: 000000000000000000000000D93144271FAF8157
WWN: 2293-0001-55b0-cd0b               PreferredCtrlId: N/A
RAIDLevel: RAID5                       StripeSize: 128KB
Capacity: 10TB                         PhysicalCapacity: 12TB
ReadPolicy: ReadAhead                  WritePolicy: WriteBack
CurrentWritePolicy: WriteBack
NumOfUsedPD: 6                         NumOfAxles: 1
SectorSize: 512Bytes                   RAID5&6Algorithm: right asymmetric (4)
TolerableNumOfDeadDrivesPerAxle: 1     ParityPace: N/A
CodecScheme: N/A


"""


class LogDrvOverviewParserTest(unittest.TestCase):

    def test_none_should_return_empty_list(self):
        subject = LogDrvOverviewParser(None)

        self.assertEqual([], subject.drives)

    def test_single_drive_should_work(self):
        subject = LogDrvOverviewParser(SINGLE_DRIVE)

        drive0 = subject.drives[0]
        self.assertEqual(0, drive0.drive_id)
        self.assertEqual('000000000000000000000000D93144271FAF8157', drive0.serial)
        self.assertEqual('2293-0001-55b0-cd0b', drive0.wwn)
        self.assertTrue(drive0.synced)
        self.assertTrue(drive0.operational)
        self.assertEqual('10TB', drive0.capacity)
        self.assertEqual('12TB', drive0.physical_capacity)