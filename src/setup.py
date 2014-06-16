#!/usr/bin/env python
# coding=utf-8

# Copyright 2014 Dirk Dittert
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
#      requires=['mock==1.0.1'],
      install_requires=['requests==2.3.0', 'psutil==2.1.1'],
      entry_points = {
          'console_scripts' : [
              'pyprobe = pyprobe.probe:main'
          ]
      }
)
