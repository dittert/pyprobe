# coding=utf-8
import re

from pyprobe import Final, ValueType, ModeType

__author__ = 'Dirk Dittert'


class SmartAttribute(object):
    """
    Represents the value of one SMART attribute.
    """

    def __init__(self, attrid, name, flag, value, worst, threshold, stype, updated, when_failed, raw_value):
        self.attrid = int(attrid)
        self.name = name
        self.flag = flag
        self.value = int(value)
        self.worst = int(worst)
        self.threshold = int(threshold)
        self.type = stype
        self.updated = updated
        self.when_failed = when_failed
        self.raw_value = int(raw_value)

    def value_type(self):
        """
        Returns the PRTG value type for this attribute.

        :return: the type. See class ValueType for possible values.
        :rtype: unicode
        """
        if self.attrid in (190, 194):
            return ValueType.TEMPERATURE
        else:
            return ValueType.COUNT

    # noinspection PyMethodMayBeStatic
    def mode_type(self):
        """
        Returns the PRTG mode type for this attribute.

        :return: the type. See class ModeType for possible values
        :rtype: unicode
        """
        return ModeType.INTEGER

    def __repr__(self):
        return u"{}: {}".format(self.name, self.raw_value)


class SmartAttributeType(object):
    __metaclass__ = Final

    OLD_AGE = "Old_age"
    PRE_FAIL = "Pre-fail"


class SmartAttributeUpdate(object):
    __metaclass__ = Final

    ALWAYS = "Always"
    OFFLINE = "Offline"


class SmartParser(object):

    def __init__(self, content):
        """
        :type content: str
        """
        lines = content.splitlines()
        self._smart_available, self._smart_enabled = self._smart_status(lines)
        self._model = self._find_model(lines)
        self._health = self._find_health(lines)
        attributes = self._find_attributes(lines)
        self._attributes = {}
        if attributes:
            for attr in attributes:
                parts = attr.split()
                if len(parts) >= 10:
                    attr = SmartAttribute(*parts[0:10:])
                    self._attributes[attr.attrid] = attr
                else:
                    print("Unexpected attribute line: ")
                    print(attr)

    @property
    def attributes(self):
        return self._attributes

    def now_failing(self):
        """
        Determine which attributes are currently failing.

        :return: the SMART attributes that are currently failing.
        :rtype: list[SmartAttribute]
        """
        return [a for a in self._attributes.values() if a.when_failed.lower() == 'failing_now']

    def failed_in_past(self):
        """
        Determine which attributes failed in the past.

        :return: the SMART attributes that failed in the past. Currently failing attributes are not considered.
        :rtype: list[SmartAttribute]
        """
        return [a for a in self._attributes.values() if a.when_failed.lower() == 'in_the_past']

    def non_healthy_attributes(self):
        """
        Determines all attributes that failed in the past or are currently failing.

        :return: the SMART attributes that are not ok.
        :rtype: list[SmartAttribute]
        """
        return [a for a in self._attributes.values() if a.when_failed != '-']

    @property
    def health(self):
        """
        Returns the health as determined by smartcl. This value may not be available for all drives.

        :return: the overall health value.
        :rtype: str | None
        """
        return self._health

    def healthy(self):
        return self._health in ("PASSED", "OK")

    @property
    def smart_available(self):
        return self._smart_available

    @property
    def smart_enabled(self):
        return self._smart_enabled

    @property
    def model(self):
        return self._model

    @staticmethod
    def _find_attributes(lines):
        """
        :type lines: list[str]
        :rtype: list[str] | None
        """
        start_idx = -1
        end_idx = -1
        for idx, line in enumerate(lines):
            if line.startswith("Vendor Specific"):
                start_idx = idx + 2
            if len(line.strip()) == 0 and idx > start_idx != -1:
                end_idx = idx
                break
        if start_idx >= 0 and end_idx == -1:
            return lines[start_idx::]
        elif start_idx >= 0 and end_idx >= 0:
            return lines[start_idx:end_idx:]
        else:
            return None

    @staticmethod
    def _find_health(lines):
        for l in lines:
            matcher = re.search(r"SMART overall-health self-assessment test result: (.*)", l)
            if matcher:
                return matcher.group(1)
            matcher = re.search(r"SMART Health Status: (.*)", l)
            if matcher:
                return matcher.group(1)

        return None

    @staticmethod
    def _fail_for_missing_smart_capability():
        pass

    @staticmethod
    def _smart_status(lines):
        active = False
        available = False
        for l in lines:
            if l == "SMART support is: Available - device has SMART capability.":  # smartctl
                available = True
            if l in ("SMART support is: Enabled", "SMART Status: Enable"):  # Promise Pegasus
                active = True
        return available, active

    @staticmethod
    def _find_model(lines):
        for l in lines:
            matcher = re.search(r"Device Model:\s+(.*)", l)
            if matcher:
                return matcher.group(1)
            matcher = re.search(r"Model Number: (.*)", l)
            if matcher:
                return matcher.group(1)