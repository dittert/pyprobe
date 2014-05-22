# coding=utf-8
import unittest
from os import path

from pyprobe import SensorError
from pyprobe.sensors.ping.sensor_ping import PingSensor
from temporary_folder import TemporaryDirectory
from utils import ChangeToDir, arguments

RECORD_ARGS = path.join(path.dirname(path.dirname(__file__)), 'recordargs.py')
FAIL = path.join(path.dirname(path.dirname(__file__)), 'fail.py')
ERROR_MESSAGE = path.join(path.dirname(__file__), 'stderr.py')


class PingTest(unittest.TestCase):

    def test_no_method_should_throw(self):
        subject = PingSensor()
        with self.assertRaises(ValueError):
            subject.execute('1234', '127.0.0.1', {}, {})

    def test_invalid_method_should_throw(self):
        subject = PingSensor()
        with self.assertRaises(ValueError):
            subject.execute('1234', '127.0.0.1', {'method': 'invalid', 'target': '8.8.8.8'}, {})

    def test_single_ping(self):
        subject = PingSensor()
        with TemporaryDirectory() as d:
            with ChangeToDir(d):
                # when: a single ping should be sent
                subject.execute('1234',  '8.8.8.8', {'method': PingSensor.SINGLE_PING_ID}, {'executable': RECORD_ARGS})

                # then: the correct arguments are passed on the command line
                args = arguments(d)
                self.assertEqual(['-c', '1', '8.8.8.8'], args)

    def test_ping_with_different_packet_size(self):
        subject = PingSensor()
        with TemporaryDirectory() as d:
            with ChangeToDir(d):
                # when: a single ping with a custom packet size should be sent
                subject.execute('1234',  '8.8.8.8',
                                {'method': PingSensor.SINGLE_PING_ID, 'size': 300},
                                {'executable': RECORD_ARGS})

                # then: the correct arguments are passed on the command line
                args = arguments(d)
                self.assertEqual(['-c', '1', '-s', '300', '8.8.8.8'], args)

    def test_multiple_ping(self):
        subject = PingSensor()
        with TemporaryDirectory() as d:
            with ChangeToDir(d):
                # when: multiple pings should be sent
                subject.execute('1234', '8.8.8.8', {'method': PingSensor.MULTIPLE_PING_ID}, {'executable': RECORD_ARGS})

                # then: the correct arguments are passed on the command line
                args = arguments(d)
                self.assertEqual(['-c', '3', '8.8.8.8'], args)

    def test_failure(self):
        subject = PingSensor()
        with TemporaryDirectory() as d:
            # when: the ping executable exits with error code != 0
            result = subject.execute('1234', '8.8.8.8', {'method': PingSensor.MULTIPLE_PING_ID}, {'executable': FAIL})

            # then: this is considered to be an error
            self.assertIsInstance(result, SensorError)

    def test_message_on_stderror(self):
        subject = PingSensor()
        with TemporaryDirectory() as d:
            # when: the ping executable returns something on stderr
            result = subject.execute('1234', '8.8.8.8', {'method': PingSensor.MULTIPLE_PING_ID},
                                     {'executable': ERROR_MESSAGE})

            # then: this is considered to be an error.
            self.assertIsInstance(result, SensorError)
            self.assertEqual(result.message, "Error message on stderr.\n")