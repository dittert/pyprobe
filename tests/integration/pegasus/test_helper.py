# coding=utf-8
__author__ = 'Dirk Dittert'


def get_channel(result, channel_name):
    """
    :param result: The result returned by the sensor
    :type result: prtg.results.SensorResult

    :param channel_name: The name of the channel
    :type channel_name: basestring

    :return: the channel that has the given name
    :rtype: SensorChannel|None
    """
    return next((c for c in result.channel if c.name == channel_name), None)