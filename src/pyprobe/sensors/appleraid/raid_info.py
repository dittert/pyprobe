# coding=utf-8

import re

__author__ = 'Dirk Dittert'


class DiskUtilParser(object):
    def __init__(self, content):
        """
        :param content: the output of disktuil info <device>
        :type content: str
        """
        self._content = content

    def raid_info(self):
        """
        :return: information about the RAID set.
        :rtype: AppleRaidInfo | None
        """
        raid_info = None
        lines = self._content.splitlines()
        for idx, l in enumerate(lines):
            if l.strip().startswith("This disk is a RAID Set."):
                raid_info = lines[idx + 1::]
        if raid_info is None:
            # The information does not belong to a OS X Software RAID
            return None

        result = AppleRaidInfo()
        for l in raid_info:
            matcher = re.search(r"\s+Set Name:\s+(.*)$", l)
            if matcher:
                result._name = matcher.group(1)
            matcher = re.search(r"\s+RAID Set UUID:\s+(.*)$", l)
            if matcher:
                result._uuid = matcher.group(1)
            matcher = re.search(r"\s+Level Type:\s+(.*)$", l)
            if matcher:
                result._type = matcher.group(1)
            matcher = re.search(r"\s+Status:\s+(.*)$", l)
            if matcher:
                result._status = matcher.group(1)

        return result


class AppleRaidInfo(object):
    STATUS_ONLINE = "Online"
    STATUS_DEGRADED = "Degraded"

    def __init__(self):
        self._name = None
        self._uuid = None
        self._type = None
        self._status = None

    @property
    def name(self):
        return self._name

    @property
    def uuid(self):
        return self._uuid

    @property
    def raidtype(self):
        return self._type

    @property
    def status(self):
        return self._status