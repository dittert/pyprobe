#!/usr/bin/env python
# coding=utf-8
import sys

__author__ = 'Dirk Dittert'


if __name__ == '__main__':
    print u"""\
coretemp-isa-0000
Adapter: ISA adapter
Core 0:       +43.0°C  (high = +82.0°C, crit = +100.0°C)
Core 1:       +44.0°C  (high = +82.0°C, crit = +100.0°C)
Core 2:       +45.0°C  (high = +82.0°C, crit = +100.0°C)
Core 3:       +46.0°C  (high = +82.0°C, crit = +100.0°C)

coretemp-isa-0001
Adapter: ISA adapter
Core 0:       +47.0°C  (high = +82.0°C, crit = +100.0°C)
Core 1:       +48.0°C  (high = +82.0°C, crit = +100.0°C)
Core 2:       +49.0°C  (high = +82.0°C, crit = +100.0°C)
Core 3:       +50.0°C  (high = +82.0°C, crit = +100.0°C)

i5k_amb-isa-0000
Adapter: ISA adapter
Ch. 0 DIMM 0:  +63.5°C  (low  = +127.5°C, high = +127.5°C)
Ch. 0 DIMM 1:  +52.0°C  (low  = +127.5°C, high = +127.5°C)
Ch. 1 DIMM 0:  +62.0°C  (low  = +127.5°C, high = +127.5°C)
Ch. 1 DIMM 1:  +51.5°C  (low  = +127.5°C, high = +127.5°C)
Ch. 2 DIMM 0:  +55.0°C  (low  = +127.5°C, high = +127.5°C)
Ch. 2 DIMM 1:  +51.5°C  (low  = +127.5°C, high = +127.5°C)
Ch. 3 DIMM 0:  +55.5°C  (low  = +127.5°C, high = +127.5°C)
Ch. 3 DIMM 1:  +52.0°C  (low  = +127.5°C, high = +127.5°C)

""".encode(sys.stdout.encoding)