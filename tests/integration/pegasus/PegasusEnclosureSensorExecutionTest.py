# coding=utf-8
from os import path
import unittest
from pyprobe import SensorError
from pyprobe.sensors.pegasus.sensor_enclosure import PegasusEnclosureSensor

__author__ = 'Dirk Dittert'

FAKE_UTIL = path.join(path.dirname(__file__), 'pegasus.py')
BROKEN_FAN_UTIL = path.join(path.dirname(__file__), 'enclosure_broken_fan.py')
CONTROLLER_TEMPERATURE = path.join(path.dirname(__file__), 'enclosure_controller_temperature.py')
BACKPLANE_TEMPERATURE = path.join(path.dirname(__file__), 'enclosure_backplane_temperature.py')
FAIL = path.join(path.dirname(path.dirname(__file__)), 'fail.py')


class PegasusEnclosureSensorExecutionTest(unittest.TestCase):

    def test_error_code_should_be_used(self):
        subject = PegasusEnclosureSensor()
        result = subject.execute('1234', '127.0.0.1', {}, {'executable': FAIL})

        self.assertIsInstance(result, SensorError)

    def test_fan_values_should_be_correct(self):
        subject = PegasusEnclosureSensor()
        result = subject.execute('1234', '127.0.0.1', {}, {'executable': BROKEN_FAN_UTIL})

        self.assertIsInstance(result, SensorError)
        self.assertEqual(u"Lüfterdrehzahl 600 RPM ist unterhalb der Minimaldrehzahl von 800 RPM.", result.message)

    def test_controller_temperature_exceeded(self):
        subject = PegasusEnclosureSensor()
        result = subject.execute('1234', '127.0.0.1', {}, {'executable': CONTROLLER_TEMPERATURE})

        self.assertIsInstance(result, SensorError)
        self.assertEqual(u"Temperatur 65°C von Sensor 'Controller' liegt über "
                         u"dem Grenzwert 63°C (Sensorstatus: error).", result.message)

    def test_backplane_temperature_exceeded(self):
        subject = PegasusEnclosureSensor()
        result = subject.execute('1234', '127.0.0.1', {}, {'executable': BACKPLANE_TEMPERATURE})

        self.assertIsInstance(result, SensorError)
        self.assertEqual(u"Temperatur 63°C von Sensor 'Backplane' liegt über "
                         u"dem Grenzwert 50°C (Sensorstatus: error).", result.message)

    def test_ordering_of_channels_should_be_correct(self):
        subject = PegasusEnclosureSensor()
        result = subject.execute('1234', '127.0.0.1', {}, {'executable': FAKE_UTIL})

        actual = [r.name for r in result.channel]
        self.assertEqual([u'Controller Temperatur', u'Backplane Temperatur', u'Lüfterdrehzahl'], actual)
