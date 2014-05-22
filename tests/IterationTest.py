# coding=utf-8
from pyprobe.iteration import Iteration, IllegalOrderException
import unittest

__author__ = 'Dirk Dittert'


class IterationTest(unittest.TestCase):

    def test_negative_period_should_fail(self):
        with self.assertRaises(ValueError):
            Iteration(-1)

    def test_stop_before_start_should_fail(self):
        with self.assertRaises(IllegalOrderException):
            iteration = Iteration(60)
            iteration.stop_timer()

    def test_duration(self):
        # wenn: eine Iteration kürzer als die Periode gedauert hat
        iteration = Iteration(60)
        iteration._start_time = 3.0
        iteration._end_time = 6.0

        # dann: wird bis zum Ende der Periode gewartet
        # noinspection PyProtectedMember
        self.assertEqual(57.0, iteration._time_to_next_iteration())

    def test_negative_duration_should_be_prevented(self):
        # wenn: eine Iteration, die länger gedauert hat als die Periode
        iteration = Iteration(60)
        iteration._start_time = 3.0
        iteration._end_time = 120.0

        # dann: beträgt die Wartezeit 0
        # noinspection PyProtectedMember
        self.assertEqual(0.0, iteration._time_to_next_iteration())

if __name__ == '__main__':
    unittest.main()
