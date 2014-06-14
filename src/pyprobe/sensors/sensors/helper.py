# coding=utf-8
__author__ = 'Dirk Dittert'

def determine_executable(configuration):
    return configuration.get('executable', "/usr/bin/sensors")
