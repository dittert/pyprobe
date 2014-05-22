# coding=utf-8

__author__ = 'Dirk Dittert'


# noinspection PyMethodMayBeStatic
class BaseSensor(object):
    """
    Base class for PRTG sensors. Sensors should have a no-arg constructor. The must not contain any state because
    sensor instances will be reused for different instances of a sensor (i.e. sensors of the same kind but with
    different sensor ids).
    """

    def define(self, configuration):
        """
        Returns the definition of this sensor. The definition is forwarded to the server when the probe announces
        itself. The description must not change after the first announcement.

        :param configuration: the configuration of this sensor.
        :type configuration: dict[str, str]

        :return: the metadata of this sensor or None if the sensor is not applicable for this system.
        :rtype: pyprobe.descriptions.SensorDescription | None
        """
        raise NotImplemented()

    def execute(self, sensorid, host, parameters, configuration):
        """
        Perform the action of the sensor and return the result of the check. It is assumed that the dicts that are
        passed into this method are not changed by the sensor.

        :param sensorid: the id of the sensor.
        :type sensorid: str

        :param host: the host for this sensor.
        :type host: str

        :param parameters: The parameters for this sensor.
        :type parameters: dict[str, str]

        :param configuration: The configuration for this sensor.
        :type configuration: dict[str, str]

        :return: a JSON serializable object that will be returned to the server. The object is required to have
                 a method `jsonfields` that returns a dict of fields that should be contained in the JSON response to
                 the server. It is recommended to build a response by using the `SensorError` and `SensorResult`
                 classes.
        """
        raise NotImplemented()
