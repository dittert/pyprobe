# coding=utf-8
import re

__author__ = 'Dirk Dittert'


class EnclosureParser(object):
    def __init__(self, content):
        matcher = re.search(r"CtrlWarningTempThreshold: (\d+)C", content)
        if matcher:
            self._warning_threshold = int(matcher.group(1))

        matcher = re.search(r"CtrlCriticalTempThreshold: (\d+)C", content)
        if matcher:
            self._error_threshold = int(matcher.group(1))

        matcher = re.search(r"MaxNumOfPhyDrvSlots: (\d+)", content)
        if matcher:
            self._drive_count = int(matcher.group(1))

        matcher = re.search(r"Backplane\s+(.*?)\s+> (\d+) RPM\s+(\d+) RPM", content)
        if matcher:
            self._fan = EnclosureFan(matcher.group(1), int(matcher.group(2)), int(matcher.group(3)))

        self._temperatures = [EnclosureTemperature(m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)) for m in
                              re.finditer(r"\d+\s+(.*?)\s+< (\d+)C/\d+F\s+(\d+)C/\d+F\s+(.*?)\s+", content)]

    def warning_threshold(self):
        return self._warning_threshold

    def error_threshold(self):
        return self._error_threshold

    def drive_count(self):
        return self._drive_count

    def fan(self):
        """
        :return: the enclosure fan.
        :rtype: EnclosureFan
        """
        return self._fan

    def temperatures(self):
        """
        :return: the temperature sensors of this enclosure.
        :rtype list[EnclosureTemperature]
        """
        return self._temperatures


class EnclosureFan(object):
    OK = "Functional"

    def __init__(self, status, threshold, speed):
        self.status = status
        self.threshold = threshold
        self.speed = speed

    def ok(self):
        return self.status == self.OK and self.speed > self.threshold

    def __repr__(self):
        if self.ok():
            return u"Backplane Lüfter @ {} RPM".format(self.speed)
        else:
            return u"Fehlerhafter Backplane Lüfter"


class EnclosureTemperature(object):
    OK = "normal"

    def __init__(self, name, threshold, value, status):
        self.name = name
        self.threshold = threshold
        self.value = value
        self.status = status

    def ok(self):
        return self.status == self.OK and self.value < self.threshold

    def __repr__(self):
        return "{} ({}°C)".format(self.name, self.value)
