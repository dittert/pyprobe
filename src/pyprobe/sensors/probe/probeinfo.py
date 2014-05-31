# coding=utf-8
__author__ = 'dirk'


class ProbeInfo:

    def __init__(self):
        self._count = 0
        self._bytes = 0

    def record_count(self, count):
        self._count += count

    def record_bytes(self, bytes):
        self._bytes += bytes

    def record_header(self, header):
        for key, value in header.items():
            self._bytes += len(key)
            self._bytes += len(value)

    def count(self):
        return self._count

    def bytes(self):
        return self._bytes