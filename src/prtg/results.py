__author__ = 'Dirk Dittert'


class ErrorType(object):
    DATA = 'Data'
    RESPONSE = 'Response'
    EXCEPTION = 'Exception'
    SOCKET = 'Socket'


class ValueType(object):
    BYTES_BANDWITH = 'BytesBandwidth'
    BYTES_MEMORY = 'BytesMemory'
    BYTES_DiSK = 'BytesDisk'
    BYTES_FILE = 'BytesFile'
    TIME_RESPONSE = 'TimeResponse'
    TIME_SECONDS = 'TimeSeconds'
    TIME_HOURS = 'TimeHours'
    TEMPERATURE = 'Temperature'
    PERCENT = 'Percent'
    COUNT = 'Count'
    CPU = 'CPU'
    CUSTOM = 'Custom'


class SensorResult(object):
    pass


class SensorError(object):
    def __init__(self, sensorid, code, message, error=ErrorType.RESPONSE):
        self.sensorid = sensorid
        self.code = code
        self.message = message
        self.error = error

    def jsonfields(self):
        return {
            'sensorid': self.sensorid,
            'error': self.error,
            'code': self.code,
            'message': self.message,
        }
