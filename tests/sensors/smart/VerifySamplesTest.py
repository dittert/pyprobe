import unittest
from os import path
from pyprobe.sensors.pegasus.helper import reformat_smart_values
from pyprobe.sensors.smart.smart_parser import SmartParser

__author__ = 'Dirk Dittert'


class SmartParserTest(unittest.TestCase):

    def test_correct_attributes_for_hd(self):
        with open(path.join(path.dirname(__file__), "hd.txt"), "r") as f:
            content = ''.join(f.readlines())
            parser = SmartParser(content)

            expected = [1, 3, 4, 5, 7, 9, 10, 12, 184, 187, 188, 189, 190, 194, 195, 197, 198, 199]
            actual = sorted([a.attrid for a in parser.attributes.values()])
            self.assertEqual(expected, actual)
            self.assertEqual(0, len(parser.now_failing()))

    def test_correct_attributes_for_linux(self):
        with open(path.join(path.dirname(__file__), "linux.txt"), "r") as f:
            content = ''.join(f.readlines())
            parser = SmartParser(content)

            expected = [1, 3, 4, 5, 7, 9, 10, 11, 12, 192, 193, 194, 196, 197, 198, 199, 200]
            actual = sorted([a.attrid for a in parser.attributes.values()])
            self.assertEqual(expected, actual)
            self.assertEqual(0, len(parser.now_failing()))

    def test_correct_attributes_for_promise_pegasus1(self):
        with open(path.join(path.dirname(__file__), "promise_pegasus1.txt"), "r") as f:
            content = ''.join(f.readlines())
            content = reformat_smart_values(content)
            parser = SmartParser(content)

            expected = [1, 2, 3, 4, 5, 7, 8, 9, 10, 12, 192, 193, 194, 196, 197, 198, 199]
            actual = sorted([a.attrid for a in parser.attributes.values()])
            self.assertEqual(expected, actual)
            self.assertEqual(0, len(parser.now_failing()))

    def test_correct_attributes_for_failed1(self):
        with open(path.join(path.dirname(__file__), "smart_failed1.txt"), "r") as f:
            content = ''.join(f.readlines())
            parser = SmartParser(content)

            expected = [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 181, 191, 192, 194, 195, 196, 197, 198, 199, 200, 223, 225]
            actual = sorted([a.attrid for a in parser.attributes.values()])
            self.assertEqual(expected, actual)

    def test_correct_failing_attributes_for_failed1(self):
        with open(path.join(path.dirname(__file__), "smart_failed1.txt"), "r") as f:
            content = ''.join(f.readlines())
            parser = SmartParser(content)

            actual = parser.now_failing()
            self.assertEqual(1, len(actual))
            self.assertEqual('Spin_Up_Time', actual[0].name)

    def test_correct_attributes_for_failed2(self):
        with open(path.join(path.dirname(__file__), "smart_failed2.txt"), "r") as f:
            content = ''.join(f.readlines())
            parser = SmartParser(content)

            expected = [1, 2, 5, 9, 12, 13, 100, 103, 170, 171, 172, 173, 174, 184, 187, 188, 194, 196, 198, 199]
            actual = sorted([a.attrid for a in parser.attributes.values()])
            self.assertEqual(expected, actual)

    def test_correct_failing_attributes_for_failed2(self):
        with open(path.join(path.dirname(__file__), "smart_failed2.txt"), "r") as f:
            content = ''.join(f.readlines())
            parser = SmartParser(content)

            failing_attrs = parser.now_failing()
            expected = [100, 170, 173, 174, 188, 194, 199]
            actual = sorted([a.attrid for a in failing_attrs])
            self.assertEqual(expected, actual)

    def test_correct_attributes_for_failed3(self):
        with open(path.join(path.dirname(__file__), "smart_failed3.txt"), "r") as f:
            content = ''.join(f.readlines())
            parser = SmartParser(content)

            expected = [1, 3, 4, 5, 7, 9, 10, 12, 184, 187, 188, 189, 190, 194, 195, 197, 198, 199, 240, 241, 242]
            actual = sorted([a.attrid for a in parser.attributes.values()])
            self.assertEqual(expected, actual)

    def test_correct_failing_attributes_for_failed3(self):
        with open(path.join(path.dirname(__file__), "smart_failed3.txt"), "r") as f:
            content = ''.join(f.readlines())
            parser = SmartParser(content)

            failing_attrs = parser.now_failing()
            expected = [5]
            actual = sorted([a.attrid for a in failing_attrs])
            self.assertEqual(expected, actual)

            past_failues = parser.failed_in_past()
            expected = [190]
            actual = sorted([a.attrid for a in past_failues])
            self.assertEqual(expected, actual)
