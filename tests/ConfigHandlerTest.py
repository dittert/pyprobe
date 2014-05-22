# coding=utf-8
from os import path
import unittest
import textwrap
from pyprobe.configuration import ConfigHandler, InvalidConfig
from temporary_folder import TemporaryDirectory

VALID_CONFIG = u"""
                   [General]
                   key = abc
                   name = SampleProbe
                   interval = 200
                   host = https://some.probe.de
                   """


class ConfigHandlerTest(unittest.TestCase):

    def test_missing_config_should_throw(self):
        with TemporaryDirectory() as d:
            config_file = path.join(d, u"missing.cfg")
            state_file = path.join(d, u"state")
            with self.assertRaises(ValueError):
                ConfigHandler(config_file, state_file)

    def _create_config_and_state(self, directory, config_content, state_content=None):
        """
        Creates a temporary configuration and state file in a given directory.

        :param directory: the directory to use (assumed to exist).
        :type directory: unicode

        :param config_content: the content of the configuration file.
        :type config_content: unicode

        :param state_content: the (optional) content of the state file. The state file will not be created if no
                              content is passed.
        :type state_content: unicode|None

        :return: the paths to the config and the state file.
        :rtype: (unicode, unicode)
        """
        config_content = textwrap.dedent(config_content)
        config_file = path.join(directory, u'tmp.cfg')
        with open(config_file, "w") as f:
            f.write(config_content)

        state_file = path.join(directory, u'tmp.state')
        if state_content is not None:
            with open(state_file, "w") as f:
                f.write(state_content)
        return config_file, state_file

    def test_config_should_be_detected(self):
        with TemporaryDirectory() as d:
            cf, sf = self._create_config_and_state(d, VALID_CONFIG)

            handler = ConfigHandler(cf, sf)
            cf = handler.config()

            self.assertEqual(u'abc', cf.key.key)
            self.assertEqual(u'SampleProbe', cf.probe_name)
            self.assertEqual(200, cf.base_interval)
            self.assertEqual(u'https://some.probe.de', cf.prtg_url)

    def test_missing_key_should_throw(self):
        content = u"""
                      [General]
                      name = SampleProbe
                      interval = 200
                      host = https://some.probe.de
                      """
        with TemporaryDirectory() as d:
            cf, sf = self._create_config_and_state(d, content)

            with self.assertRaises(InvalidConfig):
                ConfigHandler(cf, sf)

    def test_missing_name_should_throw(self):
        content = u"""
                      [General]
                      key = abc
                      interval = 200
                      host = https://some.probe.de
                      """
        with TemporaryDirectory() as d:
            cf, sf = self._create_config_and_state(d, content)

            with self.assertRaises(InvalidConfig):
                ConfigHandler(cf, sf)

    def test_missing_host_should_throw(self):
        content = u"""
                      [General]
                      key = abc
                      name = SampleProbe
                      interval = 200
                      """
        with TemporaryDirectory() as d:
            cf, sf = self._create_config_and_state(d, content)

            with self.assertRaises(InvalidConfig):
                ConfigHandler(cf, sf)

    def test_missing_interval_should_use_default(self):
        content = u"""
                      [General]
                      key = abc
                      name = SampleProbe
                      host = https://some.probe.de
                      """
        with TemporaryDirectory() as d:
            cf, sf = self._create_config_and_state(d, content)
            handler = ConfigHandler(cf, sf)
            config = handler.config()

            self.assertEqual(300, config.base_interval)

    def test_noconfig_for_sensor_should_return_empty_dict(self):
        with TemporaryDirectory() as d:
            cf, sf = self._create_config_and_state(d, VALID_CONFIG)
            handler = ConfigHandler(cf, sf)

            self.assertEqual(dict(), handler.config_for_sensor(u"does_not_exist"))

    def test_config_for_sensor_should_return_dict(self):
        with TemporaryDirectory() as d:
            content = u"""
                          [General]
                          key = abc
                          name = SampleProbe
                          interval = 200
                          host = https://some.probe.de

                          [sensor]
                          key = value
                          """
            cf, sf = self._create_config_and_state(d, content)
            handler = ConfigHandler(cf, sf)

            d = handler.config_for_sensor(u"sensor")
            self.assertEqual({u'key': u'value'}, d)

    def test_trailing_slash_of_url_should_be_stripped(self):
        with TemporaryDirectory() as d:
            content = u"""
                          [General]
                          key = abc
                          name = SampleProbe
                          interval = 200
                          host = https://some.probe.de/
                          """
            cf, sf = self._create_config_and_state(d, content)
            handler = ConfigHandler(cf, sf)
            subject = handler.config()

            self.assertEqual(u'https://some.probe.de', subject.prtg_url)

if __name__ == '__main__':
    unittest.main()