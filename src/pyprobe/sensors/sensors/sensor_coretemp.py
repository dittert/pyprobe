# coding=utf-8
import platform
import subprocess
from pyprobe.sensors import *
from pyprobe.sensors import BaseSensor
from pyprobe.sensors.process_helper import get_outputs_of_process
from pyprobe.sensors.sensors.LinuxCoreTemperatureParser import LinuxCoreTemperatureParser
from pyprobe.sensors.sensors.LinuxSensorsParser import LinuxSensorsParser
from pyprobe.sensors.sensors.helper import determine_executable
from pyprobe.utils import to_bytes

__author__ = 'Dirk Dittert'


class LinuxCoreTempSensor(BaseSensor):
    KIND = u'sensorscoretemp'

    ERROR_CODE_EXECUTION_ERROR = 1
    ERROR_CODE_NO_CPUS = 2

    def define(self, configuration):
        if platform.system() != "Linux":
            return None

        result = SensorDescription(u'CPU Temperatur', self.KIND)
        result.description = u'Monitort die Temperatur der CPU-Cores mit lm-sensors.'

        group = GroupDescription(u'settings', u'Einstellungen')
        field_cpus = FieldDescription(u'cpus', u'CPUs', InputTypes.EDIT)
        field_cpus.help = u'Geben Sie Namen der Sensoren an, die ausgewertet werden sollen (z.B. coretemp-isa-0000). ' \
                          u'Sie können den Sensoren mehrerer CPUs durch Komma getrennt angeben. Es werden dann die ' \
                          u'Werte aller CPUs in einem Diagramm dargestellt. Um die Temperaturen aller CPUs ' \
                          u'auszuwerten, verwenden Sie den Wert [b]alle[/b].'
        field_cpus.default = u'alle'
        group.fields.append(field_cpus)
        result.groups.append(group)
        return result

    def execute(self, sensorid, host, parameters, configuration):
        executable = determine_executable(configuration)
        command = u'LC_ALL=C {}'.format(executable)
        proc = subprocess.Popen(to_bytes(command), shell=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, out = get_outputs_of_process(proc)

        if proc.returncode != 0:
            return None

        parser = LinuxSensorsParser(out)
        if u'cpus' not in parameters or parameters[u'cpus'].strip() in (u'alle', u'all'):
            # Keine Infos welche CPU => alle
            sensors = [(name, chunk) for (t, name, chunk) in parser.sensors if t == u"coretemp-isa"]
        else:
            cpus = [x.strip().lower() for x in parameters[u'cpus'].split(',')]
            sensors = [(name, chunk) for (t, name, chunk) in parser.sensors if name in cpus]

        if len(sensors) == 0:
            return SensorError(sensorid, self.ERROR_CODE_NO_CPUS, u'Keine CPUs mit Temperatursensoren gefunden.')

        result = SensorResult(sensorid)
        for (name, chunk) in sensors:
            parser = LinuxCoreTemperatureParser(chunk)
            for t in parser.temperatures:
                channel = SensorChannel(t.cpu, ModeType.FLOAT, ValueType.TEMPERATURE, t.actual)
                channel.limit_max_warning = t.warning
                channel.limit_max_error = t.error
                result.channel.append(channel)
        return result
