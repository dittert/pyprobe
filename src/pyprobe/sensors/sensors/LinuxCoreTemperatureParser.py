# coding=utf-8
import re

__author__ = 'Dirk Dittert'


class LinuxCoreTemperatureParser:
    def __init__(self, chunk):
        self._temperatures = []

        lines = chunk.splitlines()
        if len(lines) > 2:
            matcher = re.search(r"coretemp-isa-(\d+)", lines[0])
            cpu = 1 + int(matcher.group(1))
            for l in lines[2::]:
                matcher = re.search(ur"Core (\d+):\s+\+(.*).C\s+\(high = \+(.*).C, crit = +\+(.*).C\)", l)
                if matcher:
                    temp = CoreTemperature(cpu, 1 + int(matcher.group(1)), float(matcher.group(2)), float(matcher.group(3)), float(matcher.group(4)))
                    self._temperatures.append(temp)

    @property
    def temperatures(self):
        """
        :rtype: list[CoreTemperature]
        """
        return self._temperatures


class CoreTemperature:
    def __init__(self, cpu, core, actual, high, crit):
        self._cpu = cpu
        self._core = core
        self._actual = actual
        self._high = high
        self._crit = crit

    @property
    def cpu(self):
        return u"CPU {}-{}".format(self._cpu, self._core)

    @property
    def actual(self):
        return self._actual

    @property
    def warning(self):
        return self._high

    @property
    def error(self):
        return self._crit

    def __repr__(self):
        return u"CPU {}-{}: {}°C (Warning: {}°C, Error: {}°C)".format(self._cpu, self._core, self._actual, self._high,
                                                                      self._crit)
