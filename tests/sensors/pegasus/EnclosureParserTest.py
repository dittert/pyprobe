# coding=utf-8
import unittest
from pyprobe.sensors.pegasus.enclosure import EnclosureParser

__author__ = 'Dirk Dittert'


class EnclosureParserTest(unittest.TestCase):
    HEALTHY_OUTPUT = """\

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

    def test_warning_values_should_be_detected(self):
        parser = EnclosureParser(self.HEALTHY_OUTPUT)

        self.assertEqual(63, parser.warning_threshold())
        self.assertEqual(68, parser.error_threshold())

    def test_number_of_drives(self):
        parser = EnclosureParser(self.HEALTHY_OUTPUT)

        self.assertEqual(6, parser.drive_count())

    def test_fan_status(self):
        parser = EnclosureParser(self.HEALTHY_OUTPUT)

        subject = parser.fan()
        self.assertTrue(subject.ok())
        self.assertEqual(800, subject.threshold)
        self.assertEqual(1100, subject.speed)

    def test_temperatures(self):
        parser = EnclosureParser(self.HEALTHY_OUTPUT)

        self.assertEqual(2, len(parser.temperatures()))
        self.assertEqual(['Controller', 'Backplane'], [s.name for s in parser.temperatures()])
        self.assertEqual([52, 44], [s.value for s in parser.temperatures()])
        self.assertEqual(['normal', 'normal'], [s.status for s in parser.temperatures()])