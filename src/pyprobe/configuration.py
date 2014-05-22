# coding=utf-8
__author__ = 'Dirk Dittert'

import hashlib
import json
import sys
from os import path
import codecs
import ConfigParser
from ConfigParser import NoOptionError


def _encrypt(key):
    """
    :type key: str
    :rtype: str
    """
    return hashlib.sha1(key.encode('utf-8')).hexdigest()


class ServerKey(object):
    """
    Represents a key to access the server with convenience methods to access the hashed version.
    """

    def __init__(self, key):
        """
        :type key: str
        """
        if len(key) == 0:
            raise ValueError("No API key specified to access server")

        self.key = key
        self.encrypted = _encrypt(key)

    def __repr__(self):
        """ :rtype: str """
        return self.encrypted


class ProbeConfiguration(object):
    def __init__(self):
        self._key = None
        self._gid = None
        self._prtg_url = None
        self._probe_name = None
        self._base_interval = None

    @property
    def key(self):
        """ :rtype: ServerKey """
        return self._key

    @property
    def prtg_url(self):
        """ :rtype: str """
        return self._prtg_url

    @property
    def probe_name(self):
        """
        :return: the name of the probe.
        :rtype: str
        """
        return self._probe_name

    @property
    def base_interval(self):
        """ :rtype: int """
        return self._base_interval


class InvalidConfig(ValueError):
    pass


class ConfigHandler(object):
    def __init__(self, config_file, state_file):
        """
        :param config_file: The configuration file (including path).
        :type config_file: unicode

        :param state_file: The file that is used to store internal state (including path). The file will be created
                           if it does not exist.
        :type state_file: unicode
        """
        if config_file is None:
            raise InvalidConfig("No config specified")
        if state_file is None:
            raise ValueError("state_file must be specified")

        if not path.exists(config_file) or not path.isfile(config_file):
            raise InvalidConfig("No configurtion file found in '%s'" % config_file)

        parser = ConfigParser.ConfigParser()
        with codecs.open(config_file, 'r', sys.getdefaultencoding()) as f:
            parser.readfp(f)

        config = ProbeConfiguration()
        config._probe_name = self._read_required_key(parser, u'name')
        config._key = ServerKey(self._read_required_key(parser, u'key'))
        tmp = self._read_required_key(parser, u'host')
        if tmp.endswith('/'):
            tmp = tmp[0:-1:]
        config._prtg_url = tmp
        if parser.has_option(u'General', u'interval'):
            config._base_interval = parser.getint(u'General', u'interval')
        else:
            config._base_interval = 300

        # Parse all sensor configurations
        self._sensor_configs = dict()
        for section in parser.sections():
            if section != u"General":
                tmp = dict(parser.items(section))
                self._sensor_configs[section] = tmp

        self._sh = StateFileHandler(state_file)
        config._gid = self._sh.gid

        self._config = config

    @staticmethod
    def _read_required_key(parser, key):
        try:
            return parser.get(u'General', key)
        except (KeyError, NoOptionError):
            raise InvalidConfig("Key %s must be present in section General." % key)

    def config(self):
        """
        Returns the global configuration of this probe.

        :rtype: ProbeConfiguration
        """
        return self._config

    def config_for_sensor(self, kind):
        """
        Returns the configuration parameters for a particular kind of sensor.

        :param kind: the (unique) kind of the sensor.
        :type kind: unicode

        :return: the configuration
        :rtype: dict[unicode, unicode]
        """
        if kind in self._sensor_configs:
            return self._sensor_configs[kind]
        else:
            return dict()

    def state_handler(self):
        return self._sh


class StateFileHandler(object):

    def __init__(self, state_file):
        """
        :param state_file: the path of the state file.
        :type state_file: unicode
        """
        if state_file is None:
            raise ValueError()
        self._statefile = state_file
        self.gid = None

        if path.exists(state_file):
            with open(state_file, 'r') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    if 'gid' in data:
                        self.gid = data['gid']

    def exists(self):
        return path.exists(self._statefile)

    def update_or_create(self):
        if self.gid is None:
            raise IncompleteStateError("GID must be set before updating state.")
        with open(self._statefile, 'w') as f:
            data = {
                'state_version': 1,
                'gid': self.gid
            }
            json.dump(data, f)


class IncompleteStateError(ValueError):
    pass