#!/usr/bin/env python
# coding=utf-8
__author__ = 'Dirk Dittert'

import sys

if __name__ == '__main__':
    if ['info', '/Volumes/Space'] == sys.argv[1::]:
        print """\
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
        sys.exit(0)

    if ['info', '/Volumes/Degraded'] == sys.argv[1::]:
        print """\
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
      Status:            Degraded
      Chunk Count:       45775083
"""
        sys.exit(0)



    # http://linsec.ca/blog/2013/12/07/adventures-in-appleraid/
    if ['appleraid', 'list'] == sys.argv[1::]:
        print """\
AppleRAID sets (1 found)
===============================================================================
Name:                 Space
Unique ID:            E4F03E6C-B6F9-4F37-BDCA-B846218064E2
Type:                 Mirror
Status:               Online
Size:                 1.5 TB (1499957919744 Bytes)
Rebuild:              manual
Device Node:          disk3
-------------------------------------------------------------------------------
#  DevNode   UUID                                  Status     Size
-------------------------------------------------------------------------------
0  disk1s2   2B444E72-0456-492D-931F-6B84BC37A885  Online     1499957919744
1  disk2s2   D149C0B7-7B55-4784-8477-F4E9C598FC43  Online     1499957919744
===============================================================================
===============================================================================
Name: Mirror RAID Set 2
Unique ID: DDA38703-C0FC-4BB1-B6AF-60FFB5173F3A
Type: Mirror
Status: Degraded
Size: 2.0 TB (2000054943744 Bytes)
Rebuild: automatic
Device Node: -
-------------------------------------------------------------------------------
# DevNode UUID Status Size
-------------------------------------------------------------------------------
0 disk3s2 9C55D1A7-CA4C-4C4A-BA2F-E06C8004F9F1 63% (Rebuilding)2000054943744
1 disk1s2 C9C04A3E-C018-49A1-994E-35B728433F32 Online 2000054943744
===============================================================================
===============================================================================
Name:                 Stuff_2
Unique ID:            C96F3052-8EBD-45D5-9A25-29EE23957CA9
Type:                 Mirror
Status:               Degraded
Size:                 3.0 TB (3000248958976 Bytes)
Rebuild:              automatic
Device Node:          -
-------------------------------------------------------------------------------
#  DevNode   UUID                                  Status     Size
-------------------------------------------------------------------------------
-  -none-    F3921C5D-0B94-4264-9619-0291A5147F4E  Missing/Damaged
1  disk4s2   12511D3B-A21C-4BB7-B68B-DAA5E2AC0277  Online     3000248958976
===============================================================================
"""
        sys.exit(0)