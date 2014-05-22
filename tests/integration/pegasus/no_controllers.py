#!/usr/bin/env python
# coding=utf-8

__author__ = 'Dirk Dittert'

import sys

if __name__ == '__main__':
    if ['-C', 'spath'] == sys.argv[1::]:
        print """\
===============================================================================
Type  #    Model         Alias                            WWN
===============================================================================

"Totally 0 HBA(s) and 0 Subsystem(s)\n"""
        exit(0)