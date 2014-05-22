# coding=utf-8
__author__ = 'Dirk Dittert'

import sys

class Final(type):
    # see here: http://stackoverflow.com/a/2826746
    def __new__(mcs, name, bases, classdict):
        for b in bases:
            if isinstance(b, Final):
                raise TypeError("type '{0}' is not an acceptable base type".format(b.__name__))
        return type.__new__(mcs, name, bases, dict(classdict))


def to_utf8(elem):
    """
    :param elem: the unicode string to convert to utf-8.
    :type elem: unicode

    :return: the bytes in utf-8 encoding.
    :rtype: str
    """
    if not isinstance(elem, unicode):
        raise ValueError("Unexepected content " + elem)
    return elem.encode("utf-8")


def to_bytes(elem):
    """
    :param elem: the unicode to convert to the system encoding.
    :type elem: unicode

    :return: the bytes in platform encoding.
    :rtype: str
    """
    if not isinstance(elem, unicode):
        raise ValueError("Unexepected content " + elem)
    return elem.encode(sys.getdefaultencoding())