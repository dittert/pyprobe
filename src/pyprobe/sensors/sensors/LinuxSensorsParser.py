# coding=utf-8

__author__ = 'Dirk Dittert'


class LinuxSensorsParser:

    def __init__(self, output):
        self._output = output
        self._chunks = self._split_output_in_chunks(output)

        self._sensors = []
        for chunk in self._chunks:
            first_line = chunk.split('\n', 1)[0]
            t = first_line[:-5]
            self._sensors.append((t, first_line, chunk))

    @property
    def sensors(self):
        return self._sensors

    @staticmethod
    def _split_output_in_chunks(output):
        result = []
        lines = output.splitlines()
        chunk = []
        for l in lines:
            if len(l.strip()) == 0:
                result.append("\n".join(chunk))
                chunk = []
            else:
                chunk.append(l)
        if len(chunk) > 0:
            result.append("\n".join(chunk))
        return result


