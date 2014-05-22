# coding=utf-8
import time

__author__ = 'Dirk Dittert'


class IllegalOrderException(Exception):
    """
    Signals that some of the methods were called in an unexpected order.
    """
    pass


class Iteration(object):
    def __init__(self, period):
        """
        :type period: int
        """
        if period <= 0:
            raise ValueError("Iteration periond must be >0 but was " + str(period))

        self._period = float(period)
        self._start_time = None
        self._end_time = None

    def start_timer(self):
        self._start_time = time.time()

    def stop_timer(self):
        if self._start_time is None:
            raise IllegalOrderException("start() must be called before stop()")
        self._end_time = time.time()

    def _time_to_next_iteration(self):
        """ :rtype: float """
        if self._start_time is None:
            raise IllegalOrderException("start() must be called first.")
        if self._end_time is None:
            raise IllegalOrderException("end() must be called first.")

        duration = self._end_time - self._start_time
        return max(self._period - duration, 0.0)

    def wait_until_next_iteration(self):
        duration = self._time_to_next_iteration()
        time.sleep(duration)