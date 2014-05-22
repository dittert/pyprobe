# coding=utf-8
__author__ = 'Dirk Dittert'

import unittest
from pyprobe.taskparser import TaskParser


class TasksParserTest(unittest.TestCase):
    def test_invalid_return_code_should_throw(self):
        with self.assertRaises(ValueError):
            TaskParser(400, None)

    def test_empty_result_should_return_empty_list(self):
        parser = TaskParser(200, '[]')
        subject = parser.tasks()

        self.assertEqual([], subject)

    def test_single_sensor_should_return_entry(self):
        parser = TaskParser(200, '[{"sensorid":"2390","kind":"sample1","host":"127.0.0.1","field1":"abc"}]')
        subject = parser.tasks()

        self.assertEqual(1, len(subject))
        first_sensor = subject[0]
        self.assertEqual('2390', first_sensor.sensorid)
        self.assertEqual('sample1', first_sensor.kind)
        self.assertEqual('127.0.0.1', first_sensor.host)

    def test_multiple_sensors_should_return_values(self):
        parser = TaskParser(200, '[{"sensorid":"2390","kind":"sample1","host":"127.0.0.1","field1":"abc"},'
                                 '{"sensorid":"2391","kind":"sample1","host":"127.0.0.1","field1":"abc"}]')
        subject = parser.tasks()

        self.assertEqual(2, len(subject))
        first = subject[0]
        self.assertEqual('2390', first.sensorid)
        self.assertEqual('sample1', first.kind)

        second = subject[1]
        self.assertEqual('2391', second.sensorid)
        self.assertEqual('sample1', second.kind)

    def test_custom_fields_should_be_detected(self):
        parser = TaskParser(200, '[{"sensorid":"2390","kind":"sample1","host":"127.0.0.1","field1":"abc"}]')
        tasklist = parser.tasks()

        subject = tasklist[0].parameters
        self.assertEqual(1, len(subject))
        self.assertIn('field1', subject.keys())
        self.assertIn('abc', subject.values())

    def test_no_custom_fields_should_work(self):
        parser = TaskParser(200, '[{"sensorid":"2390","kind":"sample1","host":"127.0.0.1"}]')
        task = parser.tasks()[0]

        self.assertEqual(0, len(task.parameters))

if __name__ == '__main__':
    unittest.main()
