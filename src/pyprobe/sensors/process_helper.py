# coding=utf-8
import sys

__author__ = 'Dirk Dittert'


def get_outputs_of_process(proc):
    """
    Returns stdout and stderr of the process.

    :return: the output on both streams.
    :rtype: unicode, unicode
    """

    out, err = proc.communicate()
    encoding = sys.stdout.encoding
    if out is not None:
        out = out.decode(encoding)
    if err is not None:
        err = err.decode(encoding)
    return err, out