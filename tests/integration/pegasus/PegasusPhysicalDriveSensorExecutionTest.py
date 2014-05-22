# coding=utf-8
import unittest
from os import path

from integration.pegasus.test_helper import get_channel
from pyprobe import SensorError
from pyprobe.sensors.pegasus.sensor_phy_drive import PegasusPhysicalDriveSensor


FAKE_UTIL = path.join(path.dirname(__file__), 'pegasus.py')
NO_CONTROLLERS = path.join(path.dirname(__file__), 'no_controllers.py')
FAILED_DRIVE = path.join(path.dirname(__file__), 'pegasus_drive_failure.py')


class PegasusPhysicalDriveSensorDefinitionTest(unittest.TestCase):

    def test_existing_drive_should_work(self):
        subject = PegasusPhysicalDriveSensor()
        params = {'drive': 2, 'strict': PegasusPhysicalDriveSensor.ZERO_TOLERANCE_ID}
        result = subject.execute('1234', '127.0.0.1', params, {'executable': FAKE_UTIL})
        self.assertEqual(38, get_channel(result, "Temperatur").value)
        self.assertEqual(0, get_channel(result, "Raw Read Error Rate").value)
        self.assertEqual(0, get_channel(result, "Reallocated Sector Count").value)
        self.assertEqual(0, get_channel(result, "Seek Error Rate").value)
        self.assertEqual(0, get_channel(result, "Spin Retry Count").value)
        self.assertEqual(0, get_channel(result, "Reallocated Event Count").value)
        self.assertEqual(0, get_channel(result, "Current Pending Sector").value)
        self.assertEqual(0, get_channel(result, "Offline Uncorrectable").value)

        # Channels not present for this harddrive
        self.assertIsNone(get_channel(result, "Multi Zone Error Rate"))
        self.assertIsNone(get_channel(result, "Calibration Retry Count"))

    def test_incorrect_drive_number_should_return_error(self):
        subject = PegasusPhysicalDriveSensor()
        params = {'drive': 7, 'strict': PegasusPhysicalDriveSensor.ZERO_TOLERANCE_ID}
        result = subject.execute('1234', '127.0.0.1', params, {'executable': FAKE_UTIL})

        self.assertIsInstance(result, SensorError)
        self.assertEqual(PegasusPhysicalDriveSensor.ERROR_CODE_DRIVE_NOT_FOUND, result.code)
        self.assertEqual("Drive 7 not found.", result.message)

    def test_drive_failure_should_return_error(self):
        subject = PegasusPhysicalDriveSensor()
        params = {'drive': 1, 'strict': PegasusPhysicalDriveSensor.ZERO_TOLERANCE_ID}
        result = subject.execute('1234', '127.0.0.1', params, {'executable': FAILED_DRIVE})

        self.assertIsInstance(result, SensorError)

    def test_temperature_should_be_first_sensor(self):
        subject = PegasusPhysicalDriveSensor()
        params = {'drive': 2, 'strict': PegasusPhysicalDriveSensor.ZERO_TOLERANCE_ID}
        result = subject.execute('1234', '127.0.0.1', params, {'executable': FAKE_UTIL})

        # dann: ist der Kanal für die Temperatur der Erste
        self.assertEqual("Temperatur", result.channel[0].name)

    def test_flaky_hitachi_values_should_be_corrected(self):
        subject = PegasusPhysicalDriveSensor()
        params = {'drive': 3, 'strict': PegasusPhysicalDriveSensor.ZERO_TOLERANCE_ID}
        result = subject.execute('1234', '127.0.0.1', params, {'executable': FAKE_UTIL})

        # dann: wird der Wert für Reallocated Sector Count auf 0 korrigiert (bei Hitachi werden unter Last manchmal
        # falsche Werte zurückgeliefert).
        self.assertEqual(0, get_channel(result, "Reallocated Sector Count").value)
