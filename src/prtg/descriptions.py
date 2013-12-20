__author__ = 'Dirk Dittert'

import json


class InputTypes(object):
    EDIT = 'edit'
    PASSWORD = 'password'
    INTEGER = 'integer'
    RADIO = 'radio'


class SensorDescription(object):
    def __init__(self):
        self.name = "Sample Sensor1"
        self.kind = "sample1"
        self.description = "description"
        self.help = "help"
        self.tag = "demosensor"
        self.groups = [GroupDescription('Gruppe1', 'Gruppe 1 erfasst Werte')]

    def jsonfields(self):
        return {
            'name': self.name,
            'kind': self.kind,
            'description': self.description,
            'help': self.help,
            'tag': self.tag,
            'groups': self.groups
        }


class GroupDescription(object):
    def __init__(self, name, caption):
        self.name = name
        self.caption = caption
        self.fields = [FieldDescription('field1', 'Beschreibung Feld1')]

    def jsonfields(self):
        return {
            'name': self.name,
            'caption': self.caption,
            'fields': self.fields
        }


class FieldDescription(object):
    def __init__(self, name, caption, ftype=InputTypes.EDIT):
        self.name = name
        self.type = ftype
        self.caption = caption

    def jsonfields(self):
        return {
            'name': self.name,
            'type': self.type,
            'caption': self.caption
        }


class DescriptionJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, 'jsonfields'):
            return o.jsonfields()
        else:
            return json.JSONEncoder.default(self, o)
