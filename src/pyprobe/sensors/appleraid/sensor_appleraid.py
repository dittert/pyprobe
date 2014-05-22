# coding=utf-8
import platform
import subprocess

from pyprobe import LookupRaidStatusChannel
from pyprobe.sensors import *
from pyprobe.sensors.appleraid.raid_info import DiskUtilParser, AppleRaidInfo
from pyprobe.sensors.process_helper import get_outputs_of_process
from pyprobe.utils import to_bytes


__author__ = 'Dirk Dittert'


class AppleRaidSensor(BaseSensor):
    KIND = u'appleraid'

    ERROR_CODE_NO_RAID_DRIVE = 0
    ERROR_CODE_EXECUTION = 1

    def define(self, configuration):
        if platform.system() != "Darwin":
            # sensor is only applicable on OS X systems.
            return None

        result = SensorDescription(u"Apple Software RAID", self.KIND)
        result.description = u"Monitort ein Apple Software RAID Laufwerk."
        group = GroupDescription(u"settings", u"Einstellungen")
        field_drive = FieldDescription(u"mountpoint", u"Laufwerk")
        field_drive.help = u"Geben Sie den Pfad des zu überwachende Laufwerk an. Für das Laufwerk 'Daten' geben Sie " \
                           u"beispielsweise '/Volumes/Daten' an."
        group.fields.append(field_drive)
        result.groups.append(group)
        return result

    @staticmethod
    def _determine_executable(configuration):
        return configuration.get(u'executable', u"/usr/sbin/diskutil")

    def execute(self, sensorid, host, parameters, configuration):
        if u"mountpoint" not in parameters:
            raise ValueError("Parameter mountpoint is a mandatory parameter")
        executable = self._determine_executable(configuration)
        mountpoint = parameters['mountpoint']

        command = u"LC_ALL=C {0} info {1}".format(executable, mountpoint)
        proc = subprocess.Popen(to_bytes(command), shell=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, out = get_outputs_of_process(proc)

        if proc.returncode != 0:
            message = u"{} returned with exit code {}.".format(executable, proc.returncode)
            return SensorError(sensorid, self.ERROR_CODE_EXECUTION, message, ErrorType.RESPONSE)

        parser = DiskUtilParser(out)
        info = parser.raid_info()

        if info is None:
            message = u"{} ist kein Mac OS X RAID Volume.".format(mountpoint)
            return SensorError(sensorid, self.ERROR_CODE_NO_RAID_DRIVE, message)

        result = SensorResult(sensorid)
        channel_name = u"Status"
        if info.status == AppleRaidInfo.STATUS_ONLINE:
            result.channel.append(LookupRaidStatusChannel.ok_channel(channel_name))
        elif info.status == AppleRaidInfo.STATUS_DEGRADED:
            result.channel.append(LookupRaidStatusChannel.degraded_channel(channel_name))
        else:
            result.channel.append(LookupRaidStatusChannel.failure_channel(channel_name))
            result.message = u"Unbekannter Zustand '{}' des Laufwerks.".format(info.status)
        return result