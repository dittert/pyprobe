__author__ = 'Dirk Dittert'

import unittest
from prtg.taskparser import TaskParser


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
        self.assertEqual(first_sensor.sensorid, '2390')
        self.assertEqual(first_sensor.kind, 'sample1')
        self.assertEqual(first_sensor.host, '127.0.0.1')

    def test_multiple_sensors_should_return_values(self):
        parser = TaskParser(200, '[{"sensorid":"2390","kind":"sample1","host":"127.0.0.1","field1":"abc"},'
                                 '{"sensorid":"2391","kind":"sample1","host":"127.0.0.1","field1":"abc"}]')
        subject = parser.tasks()

        self.assertEqual(2, len(subject))

if __name__ == '__main__':
    unittest.main()
