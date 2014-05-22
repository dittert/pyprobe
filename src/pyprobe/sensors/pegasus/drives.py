# coding=utf-8

import re

__author__ = 'Dirk Dittert'


class PhyDrvOverviewParser(object):
    def __init__(self, content):
        """
        Initilizes the parser with the output of promiseutil.

        :param content: The output of promiseutil -V phydrv -v
        :type content: str
        """
        self.drives = []
        parts = re.split("-------------------------------------------------------------------------------", content)
        for part in parts:
            if len(part.strip()) == 0:
                continue

            drive = PromiseDrive()
            drive.errors = None
            drive.non_rw_errors = None
            drive.read_errors = None
            drive.write_errors = None
            matcher = re.search(r"PdId: (\d+)", part)
            if matcher is not None:
                drive.drive_id = int(matcher.group(1))

            matcher = re.search(r"OperationalStatus: (.*)", part)
            if matcher is not None:
                drive.status = matcher.group(1)

            matcher = re.search(r"Location: (.*)", part)
            if matcher is not None:
                drive.location = matcher.group(1)

            matcher = re.search(r"DriveTemperature: (\d+)C", part)
            if matcher is not None:
                drive.temperature = int(matcher.group(1))

            matcher = re.search(r"^Errors: (\d+)", part, re.MULTILINE)
            if matcher is not None:
                drive.errors = int(matcher.group(1))

            matcher = re.search(r"NonRWErrors: (\d+)", part)
            if matcher is not None:
                drive.non_rw_errors = int(matcher.group(1))

            matcher = re.search(r"ReadErrors: (\d+)", part)
            if matcher is not None:
                drive.read_errors = int(matcher.group(1))

            matcher = re.search(r"WriteErrors: (\d+)", part)
            if matcher is not None:
                drive.write_errors = int(matcher.group(1))

            matcher = re.search("ConfigurableCapacity: (.*)", part)
            if matcher is not None:
                drive.capacity = matcher.group(1)

            matcher = re.search("ModelNo: (.*)", part)
            if matcher is not None:
                drive.model = matcher.group(1)
            self.drives.append(drive)

    def drive_status(self):
        """
        Returns the drive stati.

        :return: a list of drive stati of the Promise Pegasus.
        :rtype: list[PromiseDrive]
        """
        return self.drives


class PromiseDrive(object):
    STATUS_OK = "OK"

    def __init__(self):
        self.drive_id = None
        self.status = None
        self.location = None
        self.temperature = None
        self.errors = None
        self.non_rw_errors = None
        self.read_errors = None
        self.write_errors = None
        self.model = None
        self.capacity = None

    def __str__(self):
        if self.failed():
            return "Failed Drive {} {} in {}".format(self.model, self.capacity, self.location)
        else:
            return "Drive {} {} in {}".format(self.model, self.capacity, self.location)

    def warning(self):
        if self.failed():
            return False
        if self.errors + self.non_rw_errors + self.read_errors + self.write_errors > 0:
            return True

    def failed(self):
        return self.status not in ("OK", "Ok", "Rebuilding")


class LogDrvOverviewParser(object):
    def __init__(self, content):
        self._drives = []
        if content is None:
            return

        parts = re.split("-------------------------------------------------------------------------------", content)
        for part in parts:
            if len(part.strip()) == 0:
                continue

            drive = LogicalPromiseDrive()
            matcher = re.search(r"LdId: (\d+)", part)
            if matcher is not None:
                drive.drive_id = int(matcher.group(1))

            matcher = re.search(r"SYNCed: (.*)", part)
            if matcher is not None:
                drive.synced = ("Yes" == matcher.group(1))

            # Possible values might be: http://kb.promise.com/KnowledgebaseArticle10175.aspx
            # OK, Rebuilding, Missing, Dead, Stale, PFA
            matcher = re.search(r"OperationalStatus: (.*)", part)
            if matcher is not None:
                drive.operational = (matcher.group(1) in ("OK", "Ok", "Rebuilding"))
                drive.status = matcher.group(1)

            matcher = re.search(r"SerialNo: (.*)", part)
            if matcher is not None:
                drive.serial = matcher.group(1)

            matcher = re.search(r"WWN: (.*?)\s+", part)
            if matcher is not None:
                drive.wwn = matcher.group(1)

            matcher = re.search(r"PhysicalCapacity: (.*)", part)
            if matcher is not None:
                drive.physical_capacity = matcher.group(1)

            matcher = re.search(r"Capacity: (.*?)\s+", part)
            if matcher is not None:
                drive.capacity = matcher.group(1)

            self._drives.append(drive)

    @property
    def drives(self):
        """
        :return: list of logical drives of the controller
        :rtype: list[LogicalPromiseDrive]
        """
        return self._drives


class LogicalPromiseDrive(object):
    def __init__(self):
        self.drive_id = None
        """
        The number of the drive.

        :type: int | None
        """

        self.serial = None
        """
        The serial number of the drive.

        :type: str | None
        """

        self.wwn = None
        """
        Unique WWN of the drive (World Wide Name).

        :type: str | None
        """

        self.synced = None
        """
        Flag whether the array is fully synchronized.

        :type: bool | None
        """

        self.operational = None
        """
        Operational state of the array (either ok or rebuilding)

        :type: bool
        """

        self.capacity = None
        """
        Capacity, as returned by the controller (e.g. 2TB).

        :type: str | None
        """

        self.physical_capacity = None
        """
        Physical capacity, as returned by the controller (e.g. 2TB).

        :type: str | None
        """

        self.status = None
        """
        The status of the array as returned by the controller. This should be one of OK, Rebuilding, Missing, Dead,
        Stale, PFA

        :type: str | None
        """