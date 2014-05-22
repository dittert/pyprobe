# coding=utf-8
import unittest
from pyprobe.sensors.ping.sensor_ping import PingParser

__author__ = 'Dirk Dittert'

SINGLE_SUCCES = 'PING core-switch.net.2o4.de (10.10.1.254): 56 data bytes\n' \
                '64 bytes from 10.10.1.254: icmp_seq=0 ttl=62 time=8.735 ms\n\n' \
                \
                '--- core-switch.net.2o4.de ping statistics ---\n' \
                '1 packets transmitted, 1 packets received, 0.0% packet loss\n' \
                'round-trip min/avg/max/stddev = 8.735/8.735/8.735/0.000 ms\n'

MULTIPLE_FAILURE = 'PING core-switch.net.2o4.de (10.10.1.254): 56 data bytes\n' \
                   '64 bytes from 10.10.1.254: icmp_seq=0 ttl=62 time=8.735 ms\n' \
                   '64 bytes from 10.10.1.254: icmp_seq=0 ttl=62 time=8.735 ms\n' \
                   'Timeout\n\n' \
                   \
                   '--- core-switch.net.2o4.de ping statistics ---\n' \
                   '3 packets transmitted, 2 packets received, 33.3% packet loss\n' \
                   'round-trip min/avg/max/stddev = 8.735/8.735/8.735/0.000 ms\n'


class PingParserTest(unittest.TestCase):

    def test_single_success(self):
        subject = PingParser(SINGLE_SUCCES)
        self.assertTrue(subject.successful)

    def test_transmitted_count_should_be_correct(self):
        subject = PingParser(SINGLE_SUCCES)

        self.assertEqual(1, subject.transmitted)

    def test_received_count_should_be_correct(self):
        subject = PingParser(SINGLE_SUCCES)

        self.assertEqual(1, subject.received)

    def test_average_should_be_correct(self):
        subject = PingParser(SINGLE_SUCCES)

        self.assertEqual(8.735, subject.average)

    def test_mulitple_failure(self):
        subject = PingParser(MULTIPLE_FAILURE)

        self.assertFalse(subject.successful)

    def test_transmitted_count_should_be_correct_for_failures(self):
        subject = PingParser(MULTIPLE_FAILURE)

        self.assertEqual(3, subject.transmitted)

    def test_received_count_should_be_correct_for_failures(self):
        subject = PingParser(MULTIPLE_FAILURE)

        self.assertEqual(2, subject.received)

    def test_average_should_be_correct_for_failure(self):
        subject = PingParser(MULTIPLE_FAILURE)

        self.assertEqual(8.735, subject.average)

if __name__ == '__main__':
    unittest.main()