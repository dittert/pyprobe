# coding=utf-8
import subprocess
from pyprobe.sensors.pegasus.controller import PegasusControllerParser
from pyprobe.sensors.process_helper import get_outputs_of_process

__author__ = 'Dirk Dittert'


def reformat_smart_values(data=None):
    """
    Reformats the SMART output of the Pegasus device so that it is compatible with the Parser for smartctl output.
    This is necessary, because the Pegasus device has wrapped lines and extra content that regular smartctl does not
    have.

    :param data: the input.
    :type data: str | None

    :return: content that should be compatible with smartctl
    :rtype: str | None
    """
    if data is None or len(data.strip()) == 0:
        return None

    lines = data.splitlines()
    """ :type: list[str] """

    body_start = _determine_start(lines)
    # remove separator lines as they don't appear in regular smartctl outputs so that the parser does not get
    # confused
    result = lines[0:body_start - 4:]
    result.append("{}{}".format(lines[body_start - 3], lines[body_start - 2]))

    body = lines[body_start::]
    for l in xrange(0, len(body), 2):
        new_line = "{}{}".format(body[l], body[l + 1]) if l < len(body) - 1 else body[l]
        # some lines might have additional information after the regular smartctl columns (e.g. lifetime min/max
        # temperature. These should be stripped for latter processing.
        cols = new_line.split()
        if len(cols) > 10:
            result.append('   '.join(cols[0:10:]))
        elif len(new_line.strip()) > 0:
            result.append(new_line)

    return "\n".join(result) + "\n"


def _determine_start(lines):
    """
    Determines where the section listing all SMART attributes begins.

    :param lines: the input split into lines.
    :type lines: list[str]

    :return: the index of the first attribute.
    :rtype: int
    """
    cnt = 0
    for idx, val in enumerate(lines):
        if lines[idx].startswith("======"):
            cnt += 1
        if cnt == 2:
            return idx + 1


def determine_executable(configuration):
    return configuration.get('executable', "/usr/bin/promiseutil")


def determine_controllers(configuration):
    """
    :type configuration: dict[str, str]

    :return: a list of controllers
    :rtype: list[PegasusController] | None
    """

    executable = determine_executable(configuration)
    proc = subprocess.Popen("LC_ALL=C {0} -C spath".format(executable), shell=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, out = get_outputs_of_process(proc)
    if proc.returncode != 0:
        return []

    parser = PegasusControllerParser(out)
    return parser.controllers