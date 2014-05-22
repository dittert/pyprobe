# coding=utf-8
from os import path
import os
import platform
from mock import MagicMock

__author__ = 'Dirk Dittert'


class ChangeToDir(object):
    def __init__(self, directory):
        self._directory = directory
        self._old = path.curdir

    def __enter__(self):
        os.chdir(self._directory)

    # noinspection PyUnusedLocal
    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self._old)


def arguments(d):
    """
    Retrieves the arguments that were passed to the ping command.

    :return: the arguemnts as list. The first argument of argv (e.g. the name of the executable) is not present in
             the list.
    :rtype: list[str]
    """
    filename = path.join(d, 'argv.txt')
    if not path.exists(filename):
        raise ValueError("Directory '{}' does not contain file 'argv.txt'.".format(d))
    with (open(filename, 'r')) as f:
        return [tmp.strip() for tmp in f.readlines()]


class Platform():
    def __init__(self, new_platform):
        """
        Sets the current platform (i.e. platform.system()) to a new value.

        :param new_platform: the new platform.
        :type new_platform: str
        """
        self._new_platform = new_platform
        self._oldptr = None

    def __enter__(self):
        self._oldptr = platform.system
        platform.system = MagicMock(return_value=self._new_platform)

    def __exit__(self, exc_type, exc_val, exc_tb):
        platform.system = self._oldptr