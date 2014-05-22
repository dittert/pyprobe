import unittest
from os import path
from pyprobe.sensors.pegasus.helper import reformat_smart_values
from pyprobe.sensors.smart.smart_parser import SmartParser

__author__ = 'Dirk Dittert'

CONTENT = """\
SCT capabilities: 	       (0x303f)	SCT Status supported.
                    SCT Feature Control supported.
                    SCT Data Table supported.

SMART Attributes Data Structure revision number: 16
Vendor Specific SMART Attributes with Thresholds:
ID# ATTRIBUTE_NAME          FLAG     VALUE WORST THRESH TYPE      UPDATED  WHEN_FAILED RAW_VALUE
  1 Raw_Read_Error_Rate     0x002f   200   200   051    Pre-fail  Always       -       0
  3 Spin_Up_Time            0x0027   253   253   021    Pre-fail  Always       -       1125
"""

EXPECTED = [
    "  1 Raw_Read_Error_Rate     0x002f   200   200   051    Pre-fail  Always       -       0",
    "  3 Spin_Up_Time            0x0027   253   253   021    Pre-fail  Always       -       1125"
]

CONTENT_HEALTH_STATUS = """\
SATA Version is:  SATA 3.1, 6.0 Gb/s (current: 3.0 Gb/s)
Local Time is:    Thu Jan 23 22:20:30 2014 CET
SMART support is: Available - device has SMART capability.
SMART support is: Enabled

=== START OF READ SMART DATA SECTION ===
SMART overall-health self-assessment test result: PASSED

General SMART Values:
Offline data collection status:  (0x00)	Offline data collection activity
"""


class SmartParserTest(unittest.TestCase):

    def test_find_attributes(self):
        # noinspection PyProtectedMember
        attributes = SmartParser._find_attributes(CONTENT.splitlines())

        self.assertEqual(EXPECTED, attributes)

    def test_find_correct_end_of_attributes_should_work(self):
        with open(path.join(path.dirname(__file__), "smart_failed1.txt"), "r") as f:
            # noinspection PyProtectedMember
            attributes = SmartParser._find_attributes(f.readlines())

            self.assertTrue(attributes[0].startswith("  1 Raw_Read_Error_Rate"))
            self.assertTrue(attributes[22].startswith("225 Load_Cycle_Count"))
            self.assertEqual(23, len(attributes))

    def test_attributes_should_be_parsed(self):
        parser = SmartParser(CONTENT)

        expected_attributes = [p.name for p in parser.attributes.values()]
        expected_values = [p.raw_value for p in parser.attributes.values()]

        self.assertEqual(['Raw_Read_Error_Rate', 'Spin_Up_Time'], expected_attributes)
        self.assertEqual([0, 1125], expected_values)

    def test_passed_status_should_be_detected(self):
        parser = SmartParser(CONTENT_HEALTH_STATUS)

        self.assertEqual("PASSED", parser.health)

    def test_disabled_smart(self):
        with open(path.join(path.dirname(__file__), 'smart_disabled.txt'), "r") as f:
            content = ''.join(f.readlines())
            parser = SmartParser(content)

            self.assertEqual({}, parser.attributes)
            self.assertIsNone(parser.health)
            self.assertTrue(parser.smart_available)
            self.assertFalse(parser.smart_enabled)

    def test_model_should_be_found_on_linux(self):
        with open(path.join(path.dirname(__file__), "linux.txt"), "r") as f:
            content = ''.join(f.readlines())
            parser = SmartParser(content)

            self.assertEqual('WDC WD1002FBYS-01A6B0', parser.model)

    def test_model_should_be_found_on_pegasus(self):
        with open(path.join(path.dirname(__file__), "promise_pegasus1.txt"), "r") as f:
            content = ''.join(f.readlines())
            content = reformat_smart_values(content)
            parser = SmartParser(content)

            self.assertEqual('Hitachi HDS72302', parser.model)

    def test_model_should_be_found_for_disabled_smart(self):
        with open(path.join(path.dirname(__file__), "smart_disabled.txt"), "r") as f:
            content = ''.join(f.readlines())
            parser = SmartParser(content)

            self.assertEqual('ST3500320AS', parser.model)