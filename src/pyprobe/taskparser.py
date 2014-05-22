# coding=utf-8
__author__ = 'Dirk Dittert'

import json


class TaskParser(object):
    def __init__(self, returncode, content):
        """
        :type returncode: int
        :type content: unicode
        """
        if returncode != 200:
            raise ValueError("Return code == " + str(returncode))
        self.content = content

    @staticmethod
    def object_decoder(obj):
        if not u'sensorid' in obj:
            raise ValueError('sensorid missing in result')
        if not u'kind' in obj:
            raise ValueError('kind missing in result')
        if not u'host' in obj:
            raise ValueError('host missing')

        filtered_keys = [u'sensorid', u'kind', u'host']
        parameters = {k: obj[k] for k in obj if k not in filtered_keys}

        return QueryTask(obj[u'sensorid'], obj[u'kind'], obj[u'host'], parameters)

    def tasks(self):
        """
        Returns the list of tasks to perform as indicated by the server.

        :return: the list.
        :rtype: list[QueryTask]
        """
        if self.content is None or len(self.content) == 0:
            return []
        else:
            return json.loads(self.content, object_hook=TaskParser.object_decoder)


class QueryTask(object):
    """
    Represents a job to be performed by a sensor. It contains all required information for the sensor that were
    entered when the sensor was defined in the PRTG web interface.
    """

    def __init__(self, sensorid, kind, host, fields=None):
        """
        Creates a new task. This constructor is called from JSON deserialization when jobs are retrieved from the
        server.

        :param sensorid: The ID used by PRTG to identify this sensor.
        :type sensorid: unicode

        :param kind: The type of sensor. The type must be unique.
        :type kind: unicode

        :param host: the host that the sensor belongs to. Currently, the only valid value is 127.0.0.1
        :type host: unicode

        :param fields: The parameters that are specific for the sensor. There should be no PRTG related information
                       be present.
        :type fields: dict[unicode, unicode]
        """
        self._sensorid = sensorid
        self._kind = kind
        self._host = host
        self._fields = fields

    @property
    def sensorid(self):
        """
        The ID used by PRTG to identify this sensor.

        :return: the ID.
        :rtype: unicode
        """
        return self._sensorid

    @property
    def kind(self):
        """
        The type of sensor to be executed.

        :return: which sensor to execute.
        :rtype: unicode
        """
        return self._kind

    @property
    def host(self):
        """
        The host that the sensor belongs to.

        :return: The host. The value 127.0.0.1 is returned for localhost.
        :rtype: unicode

        """
        return self._host

    @property
    def parameters(self):
        """
        Returns the parameters that belong to the the actual sensor. All probe/pyprobe specific data was stripped from
        the data structure.

        :return: the parameters.
        :rtype: dict[unicode, unicode]
        """
        return self._fields