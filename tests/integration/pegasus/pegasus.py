#!/usr/bin/env python
# coding=utf-8

__author__ = 'Dirk Dittert'

import sys

if __name__ == '__main__':
    if ['-C', 'spath'] == sys.argv[1::]:
        print """\
===============================================================================
Type  #    Model         Alias                            WWN
===============================================================================
hba   1  * Pegasus R6                                     2000-0001-9999-8888

"Totally 1 HBA(s) and 0 Subsystem(s)\n"""
        exit(0)

    if ['-C', 'phydrv', '-v'] == sys.argv[1::]:
        print """\
-------------------------------------------------------------------------------
PdId: 1
OperationalStatus: OK
Alias:
PhysicalCapacity: 2TB                  ConfigurableCapacity: 2TB
UsedCapacity: 2TB                      BlockSize: 512Bytes
ConfigStatus: Array0 Seq. No.0         Location: Encl1 Slot1
ModelNo: Hitachi HDS72302
SerialNo: MN5220F9999XXX               FirmwareVersion: MN6OA5C0
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
SerialNo: MN1220F888XXXX               FirmwareVersion: MN6OA5C0
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
        exit(0)

    if ['-C', 'phydrv'] == sys.argv[1::]:
        print """\
===============================================================================
PdId Model        Type      Capacity  Location      OpStatus  ConfigStatus
===============================================================================
1    Hitachi HDS7 SATA HDD  2TB       Encl1 Slot1   OK        Array0 Seq. No.0
2    Hitachi HDS7 SATA HDD  2TB       Encl1 Slot2   OK        Array0 Seq. No.1

"""
        exit(0)

    if ['-C', 'enclosure', '-e', '1', '-v'] == sys.argv[1::]:
        print """\

-------------------------------------------------------------------------------
Enclosure Setting:

EnclosureId: 1
CtrlWarningTempThreshold: 63C/145F     CtrlCriticalTempThreshold: 68C/154F


-------------------------------------------------------------------------------
Enclosure Info and Status:

EnclosureId: 1
EnclosureType: Pegasus-R6
SEPFwVersion: 1.00
MaxNumOfControllers: 1                 MaxNumOfPhyDrvSlots: 6
MaxNumOfFans: 1                        MaxNumOfBlowers: 0
MaxNumOfTempSensors: 2                 MaxNumOfPSUs: 1
MaxNumOfBatteries: 0                   MaxNumOfVoltageSensors: 3

===============================================================================
PSU       Status
===============================================================================
1         Powered On and Functional

===============================================================================
Fan Location        FanStatus             HealthyThreshold  CurrentFanSpeed
===============================================================================
1   Backplane       Functional            > 800 RPM         1100 RPM

===============================================================================
TemperatureSensor   Location       HealthThreshold   CurrentTemp    Status
===============================================================================
1                   Controller     < 63C/145F        52C/125F       normal
2                   Backplane      < 50C/122F        44C/111F       normal

===============================================================================
VoltageSensor  Type    HealthyThreshold         CurrentVoltage  Status
===============================================================================
1              3.3V    +/- 5% (3.13 - 3.46) V   3.2V            Operational
2              5.0V    +/- 5% (4.75 - 5.25) V   5.0V            Operational
3              12.0V   +/- 10%(10.8 - 13.2) V   12.1V           Operational

"""
        exit(0)

    if ['-C', 'smart', '-a', 'list', '-p', '1', '-v'] == sys.argv[1::]:
        print """\
-------------------------------------------------------------------------------
PdId: 1
Model Number: Hitachi HDS72302
Drive Type: SATA
SMART Status: Enable
SMART Health Status: OK
SCT Status Version:                  3
SCT Version (vendor specific):       256 (0x0100)
SCT Support Level:                   1
Device State:                        SMART Off-line Data Collection executing in background (4)
Current Temperature:                    38 Celsius
Power Cycle Min/Max Temperature:     37/39 Celsius
Lifetime    Min/Max Temperature:     21/48 Celsius
Under/Over Temperature Limit Count:   0/0
Self-test execution status:      (   0)	The previous self-test routine
					completed without error or no self-test
					has ever been run.
has ever been run.
Error logging capability:        (0x01)	Error logging supported.
Short self-test routine
recommended polling time: 	 (   1) minutes.
Extended self-test routine
recommended polling time: 	 ( 255) minutes.
SCT capabilities: 	       (0x003d)	SCT Status supported.
					SCT Feature Control supported.
					SCT Data Table supported.

SMART Self-test log structure revision number: 1
No self-tests have been logged.  [To run self-tests, use: smartctl -t]

SMART Error Log Version: 1
No Errors Logged


SMART Attributes Data Structure revision number: 16
Vendor Specific SMART Attributes with Thresholds:
==============================================================================
ID# ATTRIBUTE_NAME             FLAG    VALUE WORST THRESH TYPE      UPDATED
    WHEN_FAILED  RAW_VALUE
==============================================================================
  1 Raw_Read_Error_Rate        0x000b  100   100   016    Pre-fail  Always
        -         0
  2 Throughput_Performance     0x0005  130   130   054    Pre-fail  Offline
        -         101
  3 Spin_Up_Time               0x0007  134   134   024    Pre-fail  Always
        -         425 (Average 429)
  4 Start_Stop_Count           0x0012  100   100   000    Old_age   Always
        -         34
  5 Reallocated_Sector_Ct      0x0033  100   100   005    Pre-fail  Always
        -         0
  7 Seek_Error_Rate            0x000b  100   100   067    Pre-fail  Always
        -         0
  8 Seek_Time_Performance      0x0005  138   138   020    Pre-fail  Offline
        -         25
  9 Power_On_Hours             0x0012  098   098   000    Old_age   Always
        -         17626
 10 Spin_Retry_Count           0x0013  100   100   060    Pre-fail  Always
        -         0
 12 Power_Cycle_Count          0x0032  100   100   000    Old_age   Always
        -         20
192 Power-Off_Retract_Count    0x0032  100   100   000    Old_age   Always
        -         178
193 Load_Cycle_Count           0x0012  100   100   000    Old_age   Always
        -         178
194 Temperature_Celsius        0x0002  157   157   000    Old_age   Always
        -         38 (Lifetime Min/Max 21/48)
196 Reallocated_Event_Count    0x0032  100   100   000    Old_age   Always
        -         0
197 Current_Pending_Sector     0x0022  100   100   000    Old_age   Always
        -         0
198 Offline_Uncorrectable      0x0008  100   100   000    Old_age   Offline
        -         0
199 UDMA_CRC_Error_Count       0x000a  200   200   000    Old_age   Always
        -         0


"""
        exit(0)

    if ['-C', 'smart', '-a', 'list', '-p', '2', '-v'] == sys.argv[1::]:
        print """\
-------------------------------------------------------------------------------
PdId: 6
Model Number: Hitachi HDS72302
Drive Type: SATA
SMART Status: Enable
SMART Health Status: OK
SCT Status Version:                  3
SCT Version (vendor specific):       256 (0x0100)
SCT Support Level:                   1
Device State:                        SMART Off-line Data Collection executing in background (4)
Current Temperature:                    38 Celsius
Power Cycle Min/Max Temperature:     37/39 Celsius
Lifetime    Min/Max Temperature:     21/44 Celsius
Under/Over Temperature Limit Count:   0/0
Self-test execution status:      (   0)	The previous self-test routine
					completed without error or no self-test
					has ever been run.
has ever been run.
Error logging capability:        (0x01)	Error logging supported.
Short self-test routine
recommended polling time: 	 (   1) minutes.
Extended self-test routine
recommended polling time: 	 ( 255) minutes.
SCT capabilities: 	       (0x003d)	SCT Status supported.
					SCT Feature Control supported.
					SCT Data Table supported.

SMART Self-test log structure revision number: 1
No self-tests have been logged.  [To run self-tests, use: smartctl -t]

SMART Error Log Version: 1
ATA Error Count: 3
	CR = Command Register [HEX]
	FR = Features Register [HEX]
	SC = Sector Count Register [HEX]
	SN = Sector Number Register [HEX]
	CL = Cylinder Low Register [HEX]
	CH = Cylinder High Register [HEX]
	DH = Device/Head Register [HEX]
	DC = Device Command Register [HEX]
	ER = Error register [HEX]
	ST = Status register [HEX]
Powered_Up_Time is measured from power on, and printed as
DDd+hh:mm:SS.sss where DD=days, hh=hours, mm=minutes,
SS=sec, and sss=millisec. It "wraps" after 49.710 days.

Error 3 occurred at disk power-on lifetime: 2787 hours (116 days + 3 hours)
  When the command that caused the error occurred,
  the device was active or idle.

  After command completion occurred, registers were:
  ER ST SC SN CL CH DH
  -- -- -- -- -- -- --
  84 51 01 7f e6 07 02

  Commands leading to the command that caused the error were:
  CR FR SC SN CL CH DH DC   Powered_Up_Time  Command/Feature_Name
  -- -- -- -- -- -- -- --  ----------------  --------------------
  61 80 48 00 70 10 40 00   3d+10:26:06.065  WRITE FPDMA QUEUED
  61 80 40 80 6f 10 40 00   3d+10:26:06.065  WRITE FPDMA QUEUED
  61 80 38 00 6f 10 40 00   3d+10:26:06.065  WRITE FPDMA QUEUED
  61 80 30 80 e6 07 40 00   3d+10:26:06.065  WRITE FPDMA QUEUED
  61 00 28 80 e5 07 40 00   3d+10:26:06.065  WRITE FPDMA QUEUED

Error 2 occurred at disk power-on lifetime: 2775 hours (115 days + 15 hours)
  When the command that caused the error occurred,
  the device was active or idle.

  After command completion occurred, registers were:
  ER ST SC SN CL CH DH
  -- -- -- -- -- -- --
  84 51 01 ff fb da 07

  Commands leading to the command that caused the error were:
  CR FR SC SN CL CH DH DC   Powered_Up_Time  Command/Feature_Name
  -- -- -- -- -- -- -- --  ----------------  --------------------
  61 80 38 00 fb da 40 00   2d+22:59:43.744  WRITE FPDMA QUEUED
  61 80 30 80 fb da 40 00   2d+22:59:43.744  WRITE FPDMA QUEUED
  61 80 28 80 68 a0 40 00   2d+22:59:43.743  WRITE FPDMA QUEUED
  61 80 20 00 68 a0 40 00   2d+22:59:43.743  WRITE FPDMA QUEUED
  61 80 18 80 67 a0 40 00   2d+22:59:43.743  WRITE FPDMA QUEUED

Error 1 occurred at disk power-on lifetime: 2775 hours (115 days + 15 hours)
  When the command that caused the error occurred,
  the device was active or idle.

  After command completion occurred, registers were:
  ER ST SC SN CL CH DH
  -- -- -- -- -- -- --
  84 51 01 7f 4b 99 04

  Commands leading to the command that caused the error were:
  CR FR SC SN CL CH DH DC   Powered_Up_Time  Command/Feature_Name
  -- -- -- -- -- -- -- --  ----------------  --------------------
  61 80 c0 00 a0 b2 40 00   2d+22:37:13.587  WRITE FPDMA QUEUED
  61 80 b8 80 4b 99 40 00   2d+22:37:13.586  WRITE FPDMA QUEUED
  61 80 b0 00 4b 99 40 00   2d+22:37:13.586  WRITE FPDMA QUEUED
  61 80 a8 80 9f b2 40 00   2d+22:37:13.586  WRITE FPDMA QUEUED
  61 80 a0 00 9f b2 40 00   2d+22:37:13.585  WRITE FPDMA QUEUED



SMART Attributes Data Structure revision number: 16
Vendor Specific SMART Attributes with Thresholds:
==============================================================================
ID# ATTRIBUTE_NAME             FLAG    VALUE WORST THRESH TYPE      UPDATED
    WHEN_FAILED  RAW_VALUE
==============================================================================
  1 Raw_Read_Error_Rate        0x000b  100   100   016    Pre-fail  Always
        -         0
  2 Throughput_Performance     0x0005  136   136   054    Pre-fail  Offline
        -         83
  3 Spin_Up_Time               0x0007  134   134   024    Pre-fail  Always
        -         429 (Average 427)
  4 Start_Stop_Count           0x0012  100   100   000    Old_age   Always
        -         35
  5 Reallocated_Sector_Ct      0x0033  100   100   005    Pre-fail  Always
        -         0
  7 Seek_Error_Rate            0x000b  100   100   067    Pre-fail  Always
        -         0
  8 Seek_Time_Performance      0x0005  138   138   020    Pre-fail  Offline
        -         25
  9 Power_On_Hours             0x0012  098   098   000    Old_age   Always
        -         17627
 10 Spin_Retry_Count           0x0013  100   100   060    Pre-fail  Always
        -         0
 12 Power_Cycle_Count          0x0032  100   100   000    Old_age   Always
        -         20
192 Power-Off_Retract_Count    0x0032  100   100   000    Old_age   Always
        -         202
193 Load_Cycle_Count           0x0012  100   100   000    Old_age   Always
        -         202
194 Temperature_Celsius        0x0002  157   157   000    Old_age   Always
        -         38 (Lifetime Min/Max 21/44)
196 Reallocated_Event_Count    0x0032  100   100   000    Old_age   Always
        -         0
197 Current_Pending_Sector     0x0022  100   100   000    Old_age   Always
        -         0
198 Offline_Uncorrectable      0x0008  100   100   000    Old_age   Offline
        -         0
199 UDMA_CRC_Error_Count       0x000a  200   200   000    Old_age   Always
        -         3


"""
        exit(0)

    if ['-C', 'smart', '-a', 'list', '-p', '3', '-v'] == sys.argv[1::]:
        print """\
-------------------------------------------------------------------------------
PdId: 1
Model Number: Hitachi HDS72302
Drive Type: SATA
SMART Status: Enable
SMART Health Status: OK
SCT Status Version:                  3
SCT Version (vendor specific):       256 (0x0100)
SCT Support Level:                   1
Device State:                        SMART Off-line Data Collection executing in background (4)
Current Temperature:                    37 Celsius
Power Cycle Min/Max Temperature:     36/39 Celsius
Lifetime    Min/Max Temperature:     21/48 Celsius
Under/Over Temperature Limit Count:   0/0
Self-test execution status:      (   0)	The previous self-test routine
					completed without error or no self-test
					has ever been run.
has ever been run.
Error logging capability:        (0x01)	Error logging supported.
Short self-test routine
recommended polling time: 	 (   1) minutes.
Extended self-test routine
recommended polling time: 	 ( 255) minutes.
SCT capabilities: 	       (0x003d)	SCT Status supported.
					SCT Feature Control supported.
					SCT Data Table supported.

SMART Self-test log structure revision number: 1
No self-tests have been logged.  [To run self-tests, use: smartctl -t]

SMART Error Log Version: 1
No Errors Logged


SMART Attributes Data Structure revision number: 16
Vendor Specific SMART Attributes with Thresholds:
==============================================================================
ID# ATTRIBUTE_NAME             FLAG    VALUE WORST THRESH TYPE      UPDATED
    WHEN_FAILED  RAW_VALUE
==============================================================================
  1 Raw_Read_Error_Rate        0x000b  100   100   016    Pre-fail  Always
        -         65536
  2 Throughput_Performance     0x0005  130   130   054    Pre-fail  Offline
        -         100
  3 Spin_Up_Time               0x0007  134   134   024    Pre-fail  Always
        -         425 (Average 429)
  4 Start_Stop_Count           0x0012  100   100   000    Old_age   Always
        -         34
  5 Reallocated_Sector_Ct      0x0033  100   100   005    Pre-fail  Always
        -         0
  7 Seek_Error_Rate            0x000b  100   100   067    Pre-fail  Always
        -         0
  8 Seek_Time_Performance      0x0005  135   135   020    Pre-fail  Offline
        -         26
  9 Power_On_Hours             0x0012  098   098   000    Old_age   Always
        -         17977
 10 Spin_Retry_Count           0x0013  100   100   060    Pre-fail  Always
        -         0
 12 Power_Cycle_Count          0x0032  100   100   000    Old_age   Always
        -         20
192 Power-Off_Retract_Count    0x0032  100   100   000    Old_age   Always
        -         179
193 Load_Cycle_Count           0x0012  100   100   000    Old_age   Always
        -         179
194 Temperature_Celsius        0x0002  157   157   000    Old_age   Always
        -         38 (Lifetime Min/Max 21/48)
196 Reallocated_Event_Count    0x0032  100   100   000    Old_age   Always
        -         0
197 Current_Pending_Sector     0x0022  100   100   000    Old_age   Always
        -         0
198 Offline_Uncorrectable      0x0008  100   100   000    Old_age   Offline
        -         0
199 UDMA_CRC_Error_Count       0x000a  200   200   000    Old_age   Always
        -         0


"""
        exit(0)

    if ['-C', 'smart', '-a', 'list', '-p', '7', '-v'] == sys.argv[1::]:
        print("Error (0x4020): physical drive not found")
        exit(32)

    if ['-C', 'logdrv', '-v'] == sys.argv[1::]:
        print """\

-------------------------------------------------------------------------------
LdId: 0
ArrayId: 0                             SYNCed: Yes
OperationalStatus: OK
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
        exit(0)