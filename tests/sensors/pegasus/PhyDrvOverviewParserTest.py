# coding=utf-8
import unittest
from pyprobe.sensors.pegasus.drives import PhyDrvOverviewParser

__author__ = 'Dirk Dittert'

DRIVES = """
-------------------------------------------------------------------------------
PdId: 1
OperationalStatus: OK
Alias:
PhysicalCapacity: 2TB                  ConfigurableCapacity: 2TB
UsedCapacity: 2TB                      BlockSize: 512Bytes
ConfigStatus: Array0 Seq. No.0         Location: Encl1 Slot1
ModelNo: Hitachi HDS72302
SerialNo: MN5220F3262MHK               FirmwareVersion: MN6OA5C0
DriveInterface: SATA 3Gb/s             Protocol: ATA/ATAPI-8
WriteCacheSupport: Yes                 WriteCache: Enabled
RLACacheSupport: Yes                   RLACache: Enabled
SMARTFeatureSetSupport: Yes
SMARTSelfTestSetSupport: Yes           SMARTErrorLoggingSupport: Yes
CmdQueuingSupport: NCQ                 CmdQueuing: Enabled
CmdQueueDepth: 32                      MediumErrorThreshold: 64
Errors: 0                              NonRWErrors: 0
ReadErrors: 0                          WriteErrors: 0
PowerSavingStatus: Full Power
DriveTemperature: 38C/100F             ReferenceDriveTemperature: N/A
Flags: N/A                             LastUnconfiguredFragement: N/A

-------------------------------------------------------------------------------
PdId: 2
OperationalStatus: OK
Alias:
PhysicalCapacity: 2TB                  ConfigurableCapacity: 2TB
UsedCapacity: 2TB                      BlockSize: 512Bytes
ConfigStatus: Array0 Seq. No.1         Location: Encl1 Slot2
ModelNo: Hitachi HDS72302
SerialNo: MN1220F328DTTD               FirmwareVersion: MN6OA5C0
DriveInterface: SATA 3Gb/s             Protocol: ATA/ATAPI-8
WriteCacheSupport: Yes                 WriteCache: Enabled
RLACacheSupport: Yes                   RLACache: Enabled
SMARTFeatureSetSupport: Yes
SMARTSelfTestSetSupport: Yes           SMARTErrorLoggingSupport: Yes
CmdQueuingSupport: NCQ                 CmdQueuing: Enabled
CmdQueueDepth: 32                      MediumErrorThreshold: 64
Errors: 0                              NonRWErrors: 0
ReadErrors: 0                          WriteErrors: 0
PowerSavingStatus: Full Power
DriveTemperature: 37C/98F              ReferenceDriveTemperature: N/A
Flags: N/A                             LastUnconfiguredFragement: N/A

"""

FAILED_DRIVE = """
-------------------------------------------------------------------------------
PdId: 1
OperationalStatus: Failed
Alias:
PhysicalCapacity: 2TB                  ConfigurableCapacity: 2TB
UsedCapacity: 2TB                      BlockSize: 512Bytes
ConfigStatus: Array0 Seq. No.0         Location: Encl1 Slot1
ModelNo: Hitachi HDS72302
SerialNo: MN5220F3262MHK               FirmwareVersion: MN6OA5C0
DriveInterface: SATA 3Gb/s             Protocol: ATA/ATAPI-8
WriteCacheSupport: Yes                 WriteCache: Enabled
RLACacheSupport: Yes                   RLACache: Enabled
SMARTFeatureSetSupport: Yes
SMARTSelfTestSetSupport: Yes           SMARTErrorLoggingSupport: Yes
CmdQueuingSupport: NCQ                 CmdQueuing: Enabled
CmdQueueDepth: 32                      MediumErrorThreshold: 64
Errors: 1                              NonRWErrors: 2
ReadErrors: 3                          WriteErrors: 4
PowerSavingStatus: Full Power
DriveTemperature: 38C/100F             ReferenceDriveTemperature: N/A
Flags: N/A                             LastUnconfiguredFragement: N/A

"""


class PhyDrvOverviewParserTest(unittest.TestCase):

    def test_number_of_drives_should_be_correct(self):
        parser = PhyDrvOverviewParser(DRIVES)
        drives = parser.drive_status()
        self.assertEqual(2, len(drives))

    def test_values(self):
        parser = PhyDrvOverviewParser(DRIVES)
        drives = parser.drive_status()

        drive0 = drives[0]
        self.assertEqual(1, drive0.drive_id)
        self.assertEqual("Encl1 Slot1", drive0.location)
        self.assertEqual("OK", drive0.status)
        self.assertEqual(38, drive0.temperature)
        self.assertEqual(0, drive0.errors)
        self.assertEqual(0, drive0.non_rw_errors)
        self.assertEqual(0, drive0.read_errors)
        self.assertEqual(0, drive0.write_errors)
        self.assertEqual("2TB", drive0.capacity)
        self.assertEqual("Hitachi HDS72302", drive0.model)

    def test_failures(self):
        parser = PhyDrvOverviewParser(FAILED_DRIVE)
        drives = parser.drive_status()

        drive0 = drives[0]
        self.assertEqual(1, drive0.drive_id)
        self.assertTrue(drive0.failed())
        self.assertEqual(1, drive0.errors)
        self.assertEqual(2, drive0.non_rw_errors)
        self.assertEqual(3, drive0.read_errors)
        self.assertEqual(4, drive0.write_errors)