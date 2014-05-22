#!/usr/bin/env python
# coding=utf-8

__author__ = 'Dirk Dittert'

import sys

if __name__ == '__main__':
    if ['-C', 'logdrv', '-v'] == sys.argv[1::]:
        print """\

-------------------------------------------------------------------------------
LdId: 0
ArrayId: 0                             SYNCed: No
OperationalStatus: Rebuilding
Alias:
SerialNo: 000000000000000000000000D93199999FAF9999
WWN: 1111-0001-88b8-9999               PreferredCtrlId: N/A
RAIDLevel: RAID5                       StripeSize: 128KB
Capacity: 10TB                         PhysicalCapacity: 12TB
ReadPolicy: ReadAhead                  WritePolicy: WriteBack
CurrentWritePolicy: WriteBack
NumOfUsedPD: 6                         NumOfAxles: 1
SectorSize: 512Bytes                   RAID5&6Algorithm: right asymmetric (4)
TolerableNumOfDeadDrivesPerAxle: 1     ParityPace: N/A
CodecScheme: N/A

"""