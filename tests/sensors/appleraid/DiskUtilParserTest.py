# coding=utf-8

import unittest
from pyprobe.sensors.appleraid.raid_info import DiskUtilParser

__author__ = 'Dirk Dittert'

RAID_CONTENT = """\
Device Identifier:        disk3
Device Node:              /dev/disk3
Part of Whole:            disk3
Device / Media Name:      Space

Volume Name:              Space
Escaped with Unicode:     Space

Mounted:                  Yes
Mount Point:              /Volumes/Space
Escaped with Unicode:     /Volumes/Space

File System Personality:  Journaled HFS+
Type (Bundle):            hfs
Name (User Visible):      Mac OS Extended (Journaled)
Journal:                  Journal size 114688 KB at offset 0x2baa000
Owners:                   Enabled

Content (IOContent):      Apple_HFS
OS Can Be Installed:      Yes
Media Type:               Generic
Protocol:                 SATA
SMART Status:             Not Supported
Volume UUID:              8715ECA7-3DEB-375E-8B17-485E6672CA2B

Total Size:               1.5 TB (1499957919744 Bytes) (exactly 2929605312 512-Byte-Units)
Volume Free Space:        243.2 GB (243187904512 Bytes) (exactly 474976376 512-Byte-Units)
Device Block Size:        512 Bytes

Read-Only Media:          No
Read-Only Volume:         No
Ejectable:                No

Whole:                    Yes
Internal:                 Yes
Solid State:              No
OS 9 Drivers:             No
Low Level Format:         Not supported

This disk is a RAID Set.  RAID Set Information:
  Set Name:          Space
  RAID Set UUID:     E4F03E6C-B6F9-4F37-BDCA-B846218064E2
  Level Type:        Mirror
  Status:            Online
  Chunk Count:       45775083
"""

NO_RAID_CONTENT = """\
   Device Identifier:        disk0s2
   Device Node:              /dev/disk0s2
   Part of Whole:            disk0
   Device / Media Name:      SSD

   Volume Name:              SSD
   Escaped with Unicode:     SSD

   Mounted:                  Yes
   Mount Point:              /
   Escaped with Unicode:     /

   File System Personality:  Journaled HFS+
   Type (Bundle):            hfs
   Name (User Visible):      Mac OS Extended (Journaled)
   Journal:                  Journal size 81920 KB at offset 0x1d1c000
   Owners:                   Enabled

   Partition Type:           Apple_HFS
   OS Can Be Installed:      Yes
   Recovery Disk:            disk0s3
   Media Type:               Generic
   Protocol:                 SATA
   SMART Status:             Verified
   Volume UUID:              825CA351-0528-345C-8F72-665A583A9BF7

   Total Size:               999.3 GB (999345127424 Bytes) (exactly 1951845952 512-Byte-Units)
   Volume Free Space:        425.9 GB (425890541568 Bytes) (exactly 831817464 512-Byte-Units)
   Device Block Size:        512 Bytes

   Read-Only Media:          No
   Read-Only Volume:         No
   Ejectable:                No

   Whole:                    No
   Internal:                 Yes
   Solid State:              Yes
   Device Location:          "Bay 1"

"""

class DiskUtilParserTest(unittest.TestCase):

    def test_parsing_raid_drives_should_work(self):
        parser = DiskUtilParser(RAID_CONTENT)
        result = parser.raid_info()

        self.assertEqual("Space", result.name)
        self.assertEqual("E4F03E6C-B6F9-4F37-BDCA-B846218064E2", result.uuid)
        self.assertEqual("Mirror", result.raidtype)
        self.assertEqual("Online", result.status)

    def test_parsing_regular_drives_should_work(self):
        parser = DiskUtilParser(NO_RAID_CONTENT)
        result = parser.raid_info()

        self.assertIsNone(result)