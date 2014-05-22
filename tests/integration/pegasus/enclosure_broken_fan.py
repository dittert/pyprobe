#!/usr/bin/env python
# coding=utf-8

__author__ = 'Dirk Dittert'

import sys

if __name__ == '__main__':
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
1   Backplane       Defect                > 800 RPM         600 RPM

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