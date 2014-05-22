# coding=utf-8
import unittest
import uuid
import json
from os import path
from pyprobe.configuration import StateFileHandler, IncompleteStateError
from temporary_folder import TemporaryDirectory

__author__ = 'Dirk Dittert'


class StateFileHandlerTest(unittest.TestCase):

    def test_exists(self):
        with TemporaryDirectory() as d:
            file = path.join(d, 'state.txt')
            handler = StateFileHandler(file)
            self.assertFalse(handler.exists())

    def test_update_state_without_gid_should_throw(self):
        with TemporaryDirectory() as d:
            file = path.join(d, 'state.txt')
            handler = StateFileHandler(file)
            with self.assertRaises(IncompleteStateError):
                handler.update_or_create()

    def test_update_state_should_create_file(self):
        with TemporaryDirectory() as d:
            p = path.join(d, 'state.txt')
            handler = StateFileHandler(p)
            handler.gid = str(uuid.UUID('7ecc8dd9-d897-4f4f-a6b5-5b74d690c2e3'))
            handler.update_or_create()

            # then: a file is created that stores the state of the probe.
            self.assertTrue(path.exists(p))
            with open(p, 'r') as file:
                content = json.load(file)
                self.assertEqual({'state_version': 1, 'gid': '7ecc8dd9-d897-4f4f-a6b5-5b74d690c2e3'}, content)

    def test_state_file_should_be_read_if_it_exists(self):
        with TemporaryDirectory() as d:
            p = path.join(d, 'state.txt')
            with open(p, 'w') as file:
                json.dump({'state_version': 1, 'gid': '7ecc8dd9-d897-4f4f-a6b5-5b74d690c2e3'}, file)

            # then: the GID is read from the file.
            handler = StateFileHandler(p)
            self.assertEqual(handler.gid, '7ecc8dd9-d897-4f4f-a6b5-5b74d690c2e3')

if __name__ == '__main__':
    unittest.main()