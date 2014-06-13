# coding=utf-8
import unittest
from pyprobe.sensors.sensors.LinuxSensorsParser import LinuxCoreTemperatureParser

__author__ = 'Dirk Dittert'

CPU1 = u"""\
coretemp-isa-0000
Adapter: ISA adapter
Core 0:       +46.0°C  (high = +82.0°C, crit = +100.0°C)
Core 1:       +45.0°C  (high = +83.0°C, crit = +101.0°C)
Core 2:       +43.0°C  (high = +84.0°C, crit = +102.0°C)
Core 3:       +44.0°C  (high = +85.0°C, crit = +103.0°C)
"""


class LinuxCoreTempereatureParserTest(unittest.TestCase):

    def test_core_count_should_be_correct(self):
        subject = LinuxCoreTemperatureParser(CPU1)

        self.assertEqual(4, len(subject.temperatures))

    def test_core_names_should_be_correct(self):
        subject = LinuxCoreTemperatureParser(CPU1)
        names = [n.cpu for n in subject.temperatures]

        self.assertEqual([u'CPU 1-1', u'CPU 1-2', u'CPU 1-3', u'CPU 1-4'], names)

    def test_actual_temperatures_should_be_correct(self):
        subject = LinuxCoreTemperatureParser(CPU1)
        actual_temps = [n.actual for n in subject.temperatures]

        self.assertEqual([46.0, 45.0, 43.0, 44.0], actual_temps)

    def test_warning_temperatures_should_be_correct(self):
        subject = LinuxCoreTemperatureParser(CPU1)
        actual_temps = [n.warning for n in subject.temperatures]

        self.assertEqual([82.0, 83.0, 84.0, 85.0], actual_temps)

    def test_error_temperatures_should_be_correct(self):
        subject = LinuxCoreTemperatureParser(CPU1)
        actual_temps = [n.error for n in subject.temperatures]

        self.assertEqual([100.0, 101.0, 102.0, 103.0], actual_temps)