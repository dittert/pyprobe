#!/usr/bin/env python
# coding=utf-8

__author__ = 'Dirk Dittert'

import sys

if __name__ == '__main__':
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
  FAILING_NOW         35
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
        -         1
197 Current_Pending_Sector     0x0022  100   100   000    Old_age   Always
        -         0
198 Offline_Uncorrectable      0x0008  100   100   000    Old_age   Offline
        -         0
199 UDMA_CRC_Error_Count       0x000a  200   200   000    Old_age   Always
        -         0

"""
        exit(0)