#!/usr/bin/env python
# coding=utf-8
from distutils.core import setup
from setuptools import find_packages

setup(name='pyprobe',
      version=1.0,
      description='Python implementation of a PRTG MiniProbe',
      long_description="""\
pyprobe is a Python implementation of the PRTG miniprobe interface. It provides a number of different sensors that are
useful on Unix systems.\
""",
      author='Dirk Dittert',
      author_email='dirk.dittert@googlemail.com',
      keywords=['python', 'prtg', 'miniprobe', 'monitoring'],
      license='Apache 2',
      platforms='UNIX',
      packages=find_packages(),
      requires=['mock==1.0.1'],
      install_requires=['requests==2.3.0', 'psutil==2.1.1'],
      entry_points = {
          'console_scripts' : [
              'pyprobe = pyprobe.probe:main'
          ]
      }
)