# coding=utf-8
import json

from pyprobe.utils import Final


__author__ = 'Dirk Dittert'


class InputTypes(object):
    __metaclass__ = Final

    EDIT = u'edit'
    PASSWORD = u'password'
    INTEGER = u'integer'
    RADIO = u'radio'


class SensorDescription(object):
    def __init__(self, name, kind):
        """

        :type name: unicode
        :type kind: unicode
        """
        self.name = name
        self.kind = kind
        self.description = None
        self.help = None
        self.tag = None
        self.resourceusage = 1
        self.groups = []

    def jsonfields(self):
        return {
            u'name': self.name,
            u'kind': self.kind,
            u'description': self.description,
            u'help': self.help,
            u'tag': self.tag,
            u'groups': self.groups,
            u'resourceusage': self.resourceusage
        }


class GroupDescription(object):
    def __init__(self, name, caption):
        """
        :type name: unicode
        :type caption: unicode
        """
        self.name = name
        self.caption = caption
        self.fields = []

    def jsonfields(self):
        return {
            u'name': self.name,
            u'caption': self.caption,
            u'fields': self.fields
        }


class FieldDescription(object):
    def __init__(self, name, caption, ftype=InputTypes.EDIT):
        """
        :type name: unicode
        :type caption: unicode
        :type ftype: InputTypes
        """
        self.name = name
        self.type = ftype
        self.caption = caption
        self.required = None
        self.default = None
        self.help = None
        self.minimum = None
        self.maximum = None
        self.options = None

    def jsonfields(self):
        result = {
            u'name': self.name,
            u'type': self.type,
            u'caption': self.caption
        }

        if self.required:
            result[u'required'] = u'yes'
        if not self.default is None:
            result[u'default'] = self.default
        if not self.help is None:
            result[u'help'] = self.help
        if not self.minimum is None:
            result[u'minimum'] = self.minimum
        if not self.maximum is None:
            result[u'maximum'] = self.maximum
        if not self.options is None:
            result[u'options'] = self.options
            result[u'type'] = InputTypes.RADIO

        return result


class DescriptionJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, 'jsonfields'):
            return o.jsonfields()
        else:
            return json.JSONEncoder.default(self, o)
