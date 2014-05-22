# coding=utf-8

import re

__author__ = 'Dirk Dittert'


class PegasusControllerParser(object):
    def __init__(self, contents):
        """
        :type contents: str
        """
        self.controllers = []
        """ :type controllers: list[PegasusController]"""

        for line in contents.splitlines():
            matcher = re.search(r"hba\s+(\d+).*(Pegasus R[4|6]).*(\d{4}-\d{4}-\d{4}-\d{4})", line)
            if matcher is not None:
                controller = PegasusController()
                controller.controller_id = int(matcher.group(1))
                controller.type = matcher.group(2)
                controller.wwn = matcher.group(3)
                self.controllers.append(controller)


class PegasusController(object):
    PEGASUS_R4 = "Pegasus R4"
    PEGASUS_R6 = "Pegasus R6"

    def __init__(self):
        self.controller_id = None
        self.type = None
        self.wwn = None

    def max_drives(self):
        if self.type == PegasusController.PEGASUS_R4:
            return 4
        elif self.type == PegasusController.PEGASUS_R6:
            return 6
        else:
            raise ValueError("Unknown controller type: {0}".format(self.type))

    def __str__(self):
        return "{} ({})".format(self.type, self.controller_id)