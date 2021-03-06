# coding=utf-8
import unittest
from pyprobe.sensors.sensors.LinuxSensorsParser import LinuxSensorsParser

__author__ = 'Dirk Dittert'

SAMPLE_OUTPUT = u"""\
coretemp-isa-0000
Adapter: ISA adapter
Core 0:       +46.0°C  (high = +82.0°C, crit = +100.0°C)
Core 1:       +45.0°C  (high = +82.0°C, crit = +100.0°C)
Core 2:       +43.0°C  (high = +82.0°C, crit = +100.0°C)
Core 3:       +43.0°C  (high = +82.0°C, crit = +100.0°C)

coretemp-isa-0001
Adapter: ISA adapter
Core 0:       +43.0°C  (high = +82.0°C, crit = +100.0°C)
Core 1:       +41.0°C  (high = +82.0°C, crit = +100.0°C)
Core 2:       +43.0°C  (high = +82.0°C, crit = +100.0°C)
Core 3:       +44.0°C  (high = +82.0°C, crit = +100.0°C)

i5k_amb-isa-0000
Adapter: ISA adapter
Ch. 0 DIMM 0:  +63.5°C  (low  = +127.5°C, high = +127.5°C)
Ch. 0 DIMM 1:  +52.0°C  (low  = +127.5°C, high = +127.5°C)
Ch. 1 DIMM 0:  +62.0°C  (low  = +127.5°C, high = +127.5°C)
Ch. 1 DIMM 1:  +51.5°C  (low  = +127.5°C, high = +127.5°C)
Ch. 2 DIMM 0:  +55.0°C  (low  = +127.5°C, high = +127.5°C)
Ch. 2 DIMM 1:  +51.5°C  (low  = +127.5°C, high = +127.5°C)
Ch. 3 DIMM 0:  +55.5°C  (low  = +127.5°C, high = +127.5°C)
Ch. 3 DIMM 1:  +52.0°C  (low  = +127.5°C, high = +127.5°C)

"""


class LinuxSensorsParserTest(unittest.TestCase):

    def test_sensor_names_should_be_correct(self):
        subject = LinuxSensorsParser(SAMPLE_OUTPUT)
        names = [name for (t, name, chunk) in subject.sensors]
        self.assertEqual([u'coretemp-isa-0000', u'coretemp-isa-0001', u'i5k_amb-isa-0000'], names)

    def test_sensor_types_should_be_correct(self):
        subject = LinuxSensorsParser(SAMPLE_OUTPUT)
        types = [t for (t, name, chunk) in subject.sensors]
        self.assertEqual([u'coretemp-isa', u'coretemp-isa', u'i5k_amb-isa'], types)
