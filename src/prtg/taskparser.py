__author__ = 'Dirk Dittert'

import json

class TaskParser(object):
    def __init__(self, returncode, content):
        if returncode != 200:
            raise ValueError("Return code == " + str(returncode))
        self.content = content

    @staticmethod
    def object_decoder(obj):
        if not 'sensorid' in obj:
            raise ValueError('sensorid missing in result')
        if not 'kind' in obj:
            raise ValueError('kind missing in result')
        if not 'host' in obj:
            raise ValueError('host missing')
        return QueryTask(obj['sensorid'], obj['kind'], obj['host'])

    def tasks(self):
        parsed = json.loads(self.content, object_hook=TaskParser.object_decoder)
        return parsed


class QueryTask(object):
    def __init__(self, sensorid, kind, host, fields=None):
        self.sensorid = sensorid
        self.kind = kind
        self.host = host

    def sensorid(self):
        return self.sensorid

    def kind(self):
        return self.kind

    def host(self):
        return self.host