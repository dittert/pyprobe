# coding=utf-8
__author__ = 'dirk'


class ProbeInfo:

    def __init__(self):
        self._count = 0
        self._bytes = 0

    def record_count(self, count):
        self._count += count

    def record_bytes(self, b):
        self._bytes += b

    def record_response(self, res):
        if res.request is not None:
            if res.request.body is not None:
                self.record_bytes(len(res.request.body))
            self.record_bytes(len(res.request.url))
            self._record_header(res.request.headers)
            self._record_header(res.headers)

    def _record_header(self, header):
        for key, value in header.items():
            self._bytes += len(key)
            self._bytes += len(value)

    def count(self):
        return self._count

    def bytes(self):
        return self._bytes