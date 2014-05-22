# coding=utf-8
import re

from pyprobe.sensors.process_helper import get_outputs_of_process
from pyprobe.utils import to_bytes


__author__ = 'Dirk Dittert'

from collections import OrderedDict
import subprocess
from pyprobe.sensors import *


class PingSensor(BaseSensor):
    KIND = u'ping'
    """ Unique Kind of this sensor type. """

    SINGLE_PING_ID = u'1'
    """ Send only a single ping. """

    MULTIPLE_PING_ID = u'2'
    """ Send multiple pings. """

    def define(self, configuration):
        result = SensorDescription(u'Ping', PingSensor.KIND)
        result.description = u'Monitort die Verfügbarkeit mittels PING.'
        result.help = u'PINGs werden verwendet, um festzustellen, ob ein Gerät überhaupt per Netzwerk zu ' \
                      u'erreichen ist.'
        group = GroupDescription(u'settings', u'Ping-Einstellungen')

        field_timeout = FieldDescription(u'timeout', u'Zeitüberschreitung (Sekunden)')
        field_timeout.required = True
        field_timeout.help = u'Zeitüberschreitung in Sekunden. Maximalwert: 300.'
        field_timeout.default = 5
        field_timeout.minimum = 1
        field_timeout.maximum = 300
        group.fields.append(field_timeout)

        field_size = FieldDescription(u'size', u'Paketgröße (Bytes)')
        field_size.required = True
        field_size.default = 56
        field_size.minimum = 1
        field_size.maximum = 5000
        field_size.help = u'Die Standard-Paketgröße für Pinganfragen ist 56 Daten-Bytes (d.h. ICMP Pakete mit 64 ' \
                          u'Byte), aber Sie können eine beliebige Größe zwischen 1 und 5.000 Bytes wählen.'
        group.fields.append(field_size)

        field_method = FieldDescription(u'method', u"Pingmethode", InputTypes.RADIO)
        field_method.help = u'PRTG kann alternativ ein einzelnes Ping für einen einfachen Verfuübarkeitstest oder ' \
                            u'eine ganze Serie an Pinganfragen abschicken. Diese Mehrfachpings dienen der Messung ' \
                            u'von Paketverlusten und minimaler/maximaler Pingzeit. Eine Einstellung von "1" ist für ' \
                            u'das Verfügbarkeitsmonitoring gedacht. Verwenden Sie höhere Werte, um den Paketverlust ' \
                            u'zu ermitteln (z.B. 10 oder 100 Pinganfragen). Achtung: Bei Mehrfachpings muessen alle ' \
                            u'Anfragen fehlschlagen, um den Sensor in den Fehlerzustand zu versetzen.'

        # use an ordered dict here, because the order of items in the UI is important...
        field_method.options = OrderedDict([
            (PingSensor.SINGLE_PING_ID, u'Ein einzelnes Ping verschicken'),
            (PingSensor.MULTIPLE_PING_ID, u'Mehrfache Pinganfragen verschicken')
        ])
        field_method.default = PingSensor.SINGLE_PING_ID
        group.fields.append(field_method)

        result.groups.append(group)
        return result

    def execute(self, sensorid, host, parameters, configuration):
        if u'method' not in parameters:
            raise ValueError("Parameter method is a mandatory parameter.")
        if parameters[u'method'] != PingSensor.SINGLE_PING_ID and parameters[u'method'] != PingSensor.MULTIPLE_PING_ID:
            raise ValueError(
                "Method must be either '{}' or '{}'.".format(PingSensor.SINGLE_PING_ID, PingSensor.MULTIPLE_PING_ID))

        # check if the configuration specifies another executable (useful for testing)
        executable = configuration.get(u'executable', u'ping')

        if parameters[u'method'] == PingSensor.SINGLE_PING_ID:
            count = 1
        else:
            count = 3

        # check if a custom packet size should be used.
        if u'size' in parameters:
            tmp = int(parameters[u'size'])
            tmp = max(1, tmp)
            tmp = min(5000, tmp)
            size = u"-s %d" % tmp
        else:
            size = ""

        cmd = u"LC_ALL=C {0} -c {1} {2} {3}".format(executable, count, size, host)
        proc = subprocess.Popen(to_bytes(cmd),
                                shell=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        err, out = get_outputs_of_process(proc)

        if proc.returncode != 0:
            return SensorError(sensorid, proc.returncode, err)

        parser = PingParser(out, err)
        if not parser.successful:
            return SensorError(sensorid, 0, err)

        result = SensorResult(sensorid)
        channel = SensorChannel(name=u'Pingzeit', mode=ModeType.FLOAT, kind=ValueType.TIME_RESPONSE,
                                value=parser.average)
        result.channel.append(channel)
        return result


class PingParser(object):
    def __init__(self, out=None, err=None):
        self.successful = False
        self.transmitted = 0
        self.received = 0
        self.average = 0.0

        if out is not None:
            regex = re.compile(u"(\\d+) packets transmitted, (\\d+) packets received", re.MULTILINE)
            matcher = regex.search(out)
            if matcher is not None:
                self.transmitted = int(matcher.group(1))
                self.received = int(matcher.group(2))
                self.successful = self.transmitted == self.received

            regex = re.compile(u"^round-trip.*/([\\d\\.]+)/.*ms", re.MULTILINE)
            matcher = regex.search(out)
            if matcher is not None:
                self.average = float(matcher.group(1))
