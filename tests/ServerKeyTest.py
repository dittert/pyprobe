# coding=utf-8
__author__ = 'Dirk Dittert'

import unittest
from pyprobe.configuration import ServerKey


class ServerKeyTest(unittest.TestCase):

    def test_unencrypted_key_should_be_returned(self):
        key = ServerKey('4208b452-68c0-11e3-b117-00155d01cd00')
        self.assertEqual('4208b452-68c0-11e3-b117-00155d01cd00', key.key)

    def test_encrypted_key_should_be_returned(self):
        key = ServerKey('4208b452-68c0-11e3-b117-00155d01cd00')
        self.assertEqual('93e60af857ef87036e1d2608977238931e1a1d10', key.encrypted)

if __name__ == '__main__':
    unittest.main()