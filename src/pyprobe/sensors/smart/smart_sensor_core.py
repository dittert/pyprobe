# coding=utf-8
from pyprobe.sensors import *
from pyprobe.sensors.smart.definitions import ATTRIBUTES_EXPORTED_AS_CHANNEL, ERROR_CODE_DRIVE_FAILING, \
    ERROR_CODE_SMART_FAILURE

__author__ = 'Dirk Dittert'


def create_result_from_smart_channels(sensorid, smart_parser, zero_tolerance):
    """
    :type sensorid: unicode

    :type smart_parser: SmartParser

    :type zero_tolerance: bool

    :rtype: SensorResult | SensorError
    """
    smart_attributes = smart_parser.attributes
    non_healty_attributes = smart_parser.non_healthy_attributes()
    if len(non_healty_attributes) > 0:
        names = u", ".join([attr.name for attr in non_healty_attributes])
        if len(non_healty_attributes) > 1:
            message = u"Attributes {} indicate failure. Replace drive immediately!".format(names)
        else:
            message = u"Attribute {} indicates failure. Replace drive immediately!".format(names)
        return SensorError(sensorid, ERROR_CODE_DRIVE_FAILING, message)

    if not smart_parser.healthy():
        message = u"S.M.A.R.T. status is {}. Replace drive immediately!".format(smart_parser.health)
        return SensorError(sensorid, ERROR_CODE_SMART_FAILURE, message)

    result = SensorResult(sensorid)
    for attribute_id in ATTRIBUTES_EXPORTED_AS_CHANNEL.keys():
        if attribute_id in smart_attributes:
            smart_attr = smart_attributes[attribute_id]
            """ :type: SmartAttribute """
            channel_name = ATTRIBUTES_EXPORTED_AS_CHANNEL[attribute_id]

            channel = SensorChannel(channel_name, smart_attr.mode_type(), smart_attr.value_type(),
                                    smart_attr.raw_value)
            channel.show_chart = (channel.kind == ValueType.TEMPERATURE)
            if zero_tolerance:
                channel.limit_max_error = 1

            result.channel.append(channel)

    return result
