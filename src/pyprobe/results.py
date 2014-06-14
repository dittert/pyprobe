# coding=utf-8
from pyprobe.utils import Final

__author__ = 'Dirk Dittert'


class ErrorType(object):
    __metaclass__ = Final

    """
    Enumeration of the error types that a sensor can have.
    """

    DATA = u'Data'
    """
    The monitoried device returned a value but the sensor could not handle it.
    """

    RESPONSE = u'Response'
    """
    The monitored device reported an error. This includes timeouts, HTTP 4xx messages, etc.
    """

    EXCEPTION = u'Exception'
    """
    Error in sensor handling.
    """

    SOCKET = u'Socket'
    """
    Socket error.
    """


class ValueType(object):
    __metaclass__ = Final

    BYTES_BANDWITH = u'BytesBandwidth'
    BYTES_MEMORY = u'BytesMemory'
    BYTES_DISK = u'BytesDisk'
    BYTES_FILE = u'BytesFile'
    TIME_RESPONSE = u'TimeResponse'
    TIME_SECONDS = u'TimeSeconds'
    TIME_HOURS = u'TimeHours'
    TEMPERATURE = u'Temperature'
    PERCENT = u'Percent'
    COUNT = u'Count'
    CPU = u'CPU'
    CUSTOM = u'Custom'
    SPEED_DISK = u'SpeedDisk'
    SPEED_NET = u'SpeedNet'


class LookupRaidStatusChannel(object):
    """
    Factory class to create channels for raid array status values. Using this class requires the lookup
    pyprtg.disks.raidstatus to be installed on the core server.
    """
    __metaclass__ = Final
    LOOKUP_TABLE = u'pyprtg.disks.raidstatus'

    CODE_OK = 0
    CODE_REBUILDING = 1
    CODE_DEGRADED = 2
    CODE_FAILURE = 3

    @staticmethod
    def ok_channel(name):
        return SensorChannel(name, ModeType.INTEGER, ValueType.CUSTOM, LookupRaidStatusChannel.CODE_OK)

    @staticmethod
    def rebuilding_channel(name):
        return SensorChannel(name, ModeType.INTEGER, ValueType.CUSTOM, LookupRaidStatusChannel.CODE_REBUILDING)

    @staticmethod
    def degraded_channel(name):
        return SensorChannel(name, ModeType.INTEGER, ValueType.CUSTOM, LookupRaidStatusChannel.CODE_DEGRADED)

    @staticmethod
    def failure_channel(name):
        return SensorChannel(name, ModeType.INTEGER, ValueType.CUSTOM, LookupRaidStatusChannel.CODE_FAILURE)


class ModeType(object):
    __metaclass__ = Final

    COUNTER = u'counter'
    INTEGER = u'integer'
    FLOAT = u'float'


class SpeedTimeType(object):
    __metaclass__ = Final

    SECOND = u"Second"
    MINUTE = u"Minute"
    HOUR = u"Hour"
    DAY = u"Day"


class SizeUnitType(object):
    __metaclass__ = Final

    ONE = u'One'
    KILO = u'Kilo'
    MEGA = u'Mega'
    GIGA = u'Giga'
    TERA = u'Tera'
    BYTE = u'Byte'
    KILO_BYTE = u'KiloByte'
    MEGA_BYTE = u'MegaByte'
    GIGA_BYTE = u'GigaByte'
    TERA_BYTE = u'TeraByte'
    BIT = u'Bit'
    KILOBIT = u'KiloBit'
    MEGABIT = u'MegaBit'
    GIGABIT = u'GigaBit'
    TERABIT = u'TeraBit'


class DecimalModeType(object):
    __metaclass__ = Final

    AUTO = u'auto'
    ALL = u'all'
    CUSTOM = u'custom'


class SensorResult(object):
    def __init__(self, sensorid, message=None):
        self.sensorid = sensorid
        self.message = message
        self._channel = []

    @property
    def channel(self):
        """
        :rtype: list[SensorChannel]
        """
        return self._channel

    def jsonfields(self):
        result = {
            u'sensorid': self.sensorid,
            u'channel': self._channel
        }
        if self.message is not None:
            result[u'message'] = self.message

        return result


class SensorChannel(object):
    def __init__(self, name, mode, kind, value, customunit=None):
        """
        :param name: the (user visible) name of he channel
        :type name: unicode

        :param mode: the type of value (integer, float). See class ModeType for possible values.
        :type mode: unicode

        :param kind: the meaning of the value (e.g. percent, bytes bandwidth). See class ValueType for possible values
        :type kind: unicode

        :param value: the actual value of this channel
        :type value: int | float

        :param customunit: the custom unit for the display (or the name of the lookup that is used to represent strings)
        :type customunit: unicode | None
        """
        self.name = name
        self.mode = mode
        self.kind = kind
        self.value = value
        if (kind == ValueType.CUSTOM) and (customunit is None):
            self.customunit = u"Custom"
        elif kind == ValueType.CUSTOM:
            self.customunit = customunit
        else:
            self.customunit = None

        self.decimal_mode = None
        self.decimal_digits = None

        self.speed_size = None
        self.speed_time = None
        self.volume_size = None

        self.show_chart = True
        self.show_table = True

        self._limit_max_error = None
        self._limit_max_warning = None
        self._limit_min_error = None
        self._limit_min_warning = None
        self._limit_error_msg = None
        self._limit_warning_msg = None
        self._activate_limits = False

        self.value_lookup = None
        self.warning = False

    @property
    def activate_limits(self):
        return self._activate_limits

    @activate_limits.setter
    def activate_limits(self, activate):
        self._activate_limits = activate

    @staticmethod
    def _fail_if_not_number(value):
        if not isinstance(value, int) and not isinstance(value, float):
            raise ValueError()

    @property
    def limit_max_error(self):
        return self._limit_max_error

    @limit_max_error.setter
    def limit_max_error(self, value):
        self._fail_if_not_number(value)
        self._limit_max_error = value
        self._activate_limits = True

    @property
    def limit_max_warning(self):
        return self._limit_max_warning

    @limit_max_warning.setter
    def limit_max_warning(self, value):
        self._fail_if_not_number(value)
        self._limit_max_warning = value
        self._activate_limits = True

    @property
    def limit_min_error(self):
        return self._limit_min_error

    @limit_min_error.setter
    def limit_min_error(self, value):
        self._fail_if_not_number(value)
        self._limit_min_error = value
        self._activate_limits = True

    @property
    def limit_min_warning(self):
        return self._limit_min_warning

    @limit_min_warning.setter
    def limit_min_warning(self, value):
        self._fail_if_not_number(value)
        self._limit_min_warning = value
        self._activate_limits = True

    @property
    def limit_error_message(self):
        return self._limit_error_msg

    @limit_error_message.setter
    def limit_error_message(self, value):
        self._limit_error_msg = value
        self._activate_limits = True

    @property
    def limit_warning_message(self):
        return self._limit_warning_msg

    @limit_warning_message.setter
    def limit_warning_message(self, value):
        self._limit_warning_msg = value
        self._activate_limits = True

    def jsonfields(self):
        result = {
            u'name': self.name,
            u'mode': self.mode,
            u'kind': self.kind,
            u'value': self.value,
            u'showchart': 1 if self.show_chart else 0,
            u'showtable': 1 if self.show_table else 0,
            u'limitmode': 1 if self._activate_limits else 0
        }
        if self.customunit is not None:
            result[u'customunit'] = self.customunit
        if not self._limit_max_error is None:
            result[u'limitmaxerror'] = self._limit_max_error
        if not self._limit_max_warning is None:
            result[u'limitmaxwarning'] = self._limit_max_warning
        if not self._limit_min_error is None:
            result[u'limitminerror'] = self._limit_min_error
        if not self._limit_min_warning is None:
            result[u'limitminwarning'] = self._limit_min_warning
        if not self._limit_error_msg is None:
            result[u'limiterrormsg'] = self._limit_error_msg
        if not self._limit_warning_msg is None:
            result[u'limitwarningmsg'] = self._limit_warning_msg
        if not self.value_lookup is None:
            result[u'valuelookup'] = self.value_lookup
        if not self.speed_size is None:
            result[u'speedsize'] = self.speed_size
        if not self.speed_time is None:
            result[u'speedtime'] = self.speed_time
        if not self.volume_size is None:
            result[u'volumesize'] = self.volume_size
        if not self.decimal_mode is None:
            result[u'decimalmode'] = self.decimal_mode
        if not self.decimal_digits is None:
            result[u'decimaldigits'] = self.decimal_digits
        if self.warning:
            result[u'warning'] = 1

        return result


class SensorError(object):
    def __init__(self, sensorid, code, message, error=ErrorType.RESPONSE):
        self.sensorid = sensorid
        self.code = code
        self.message = message
        self.error = error

    def jsonfields(self):
        return {
            u'sensorid': self.sensorid,
            u'error': self.error,
            u'code': self.code,
            u'message': self.message,
        }
