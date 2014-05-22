# coding=utf-8
import platform
import subprocess

from pyprobe import LookupRaidStatusChannel
from pyprobe.sensors import *
from pyprobe.sensors.pegasus.drives import LogDrvOverviewParser
from pyprobe.sensors.pegasus.helper import determine_controllers, determine_executable
from pyprobe.sensors.process_helper import get_outputs_of_process
from pyprobe.utils import to_bytes


__author__ = 'Dirk Dittert'


class PegasusLogicalDriveSensor(BaseSensor):
    KIND = u"pegasuslogdrive"

    ERROR_CODE_EXECUTION = 1
    ERROR_CODE_NO_SUCH_DRIVE = 2
    ERROR_CODE_DRIVE_NOT_OPERATIONAL = 3
    ERROR_CODE_NOT_SYNCED = 4

    def define(self, configuration):
        if platform.system() != "Darwin":
            # sensor is only applicable on OS X systems.
            return None

        controllers = determine_controllers(configuration)
        if len(controllers) != 1:
            # no controllers available in system
            return None

        result = SensorDescription(u"Promise Promise Pegasus RAID Array", self.KIND)
        result.description = u"Monitort den Zustand eines Promise Pegasus RAID Laufwerks."

        group = GroupDescription(u"settings", u"Einstellungen")
        field_wwn = FieldDescription(u"wwn", u"WWN")
        field_wwn.help = u"Geben Sie die WWN des zu überwachenden Arrays an. Sie finden diese in den Informationen " \
                         u"zum Array im Promise Utility."
        group.fields.append(field_wwn)
        result.groups.append(group)
        return result

    def execute(self, sensorid, host, parameters, configuration):
        if u"wwn" not in parameters:
            raise ValueError("Parameter wwn is a mandatory parameter")
        wwn = parameters[u"wwn"]

        executable = determine_executable(configuration)

        command = u"LC_ALL=C {0} -C logdrv -v".format(executable)
        proc = subprocess.Popen(to_bytes(command), shell=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, out = get_outputs_of_process(proc)

        if proc.returncode != 0:
            message = u"{} returned with exit code {}.".format(executable, proc.returncode)
            return SensorError(sensorid, PegasusLogicalDriveSensor.ERROR_CODE_EXECUTION, message, ErrorType.RESPONSE)

        parser = LogDrvOverviewParser(out)
        drive = next((d for d in parser.drives if d.wwn == wwn), None)
        """ :type: LogicalPromiseDrive """

        if drive is None:
            message = u"Es wurde kein Array mit WWN '{}'  gefunden.".format(wwn)
            return SensorError(sensorid, self.ERROR_CODE_NO_SUCH_DRIVE, message, ErrorType.RESPONSE)

        result = SensorResult(sensorid)
        if drive.synced and drive.operational:
            result.channel.append(LookupRaidStatusChannel.ok_channel(u"Status"))
        elif drive.status == u"Rebuilding":
            result.channel.append(LookupRaidStatusChannel.rebuilding_channel(u"Status"))
        elif not drive.synced:
            result.channel.append(LookupRaidStatusChannel.degraded_channel(u"Status"))
        elif drive.status == u"Dead":
            result.channel.append(LookupRaidStatusChannel.failure_channel(u"Status"))
        else:
            result.message = u"Array ist in Zustand {}.".format(drive.status)
            result.channel.append(LookupRaidStatusChannel.failure_channel(u"Status"))
        return result