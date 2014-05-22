# coding=utf-8
import unittest
from os import path

from pyprobe import SensorDescription
from pyprobe.sensors.pegasus.sensor_phy_drive import PegasusPhysicalDriveSensor
from utils import Platform


FAKE_UTIL = path.join(path.dirname(__file__), 'pegasus.py')
NO_CONTROLLERS = path.join(path.dirname(__file__), 'no_controllers.py')
FAILED_DRIVE = path.join(path.dirname(__file__), 'pegasus_drive_failure.py')


class PegasusPhysicalDriveSensorDefinitionTest(unittest.TestCase):

    def test_sensor_should_not_be_available_on_linux(self):
        with Platform("Linux"):
            sensor = PegasusPhysicalDriveSensor()
            subject = sensor.define({'executable': FAKE_UTIL})

            self.assertIsNone(subject)

    def test_sensor_should_be_available_on_mac(self):
        with Platform("Darwin"):
            sensor = PegasusPhysicalDriveSensor()
            subject = sensor.define({'executable': FAKE_UTIL})

            self.assertIsNotNone(subject)

    def test_controllers_available(self):
        sensor = PegasusPhysicalDriveSensor()

        # when: there are controllers available
        subject = sensor.define({'executable': FAKE_UTIL})

        # then: a sensor definition is returned
        self.assertIsInstance(subject, SensorDescription)
        self.assertEqual(subject.kind, PegasusPhysicalDriveSensor.KIND)

    def test_no_controllers_available(self):
        sensor = PegasusPhysicalDriveSensor()

        # when: there are no controllers available
        subject = sensor.define({'executable': NO_CONTROLLERS})

        # then: None is returned
        self.assertIsNone(subject)

    def test_promiseutil_is_not_installed_should_return_none(self):
        sensor = PegasusPhysicalDriveSensor()

        # when: promiseutil is not found
        subject = sensor.define({'executable': 'ajflasfjasdlfjsaljflasdjflasjfasjdflajsdf_does_not_exist'})

        # then: None is returned
        self.assertIsNone(subject)