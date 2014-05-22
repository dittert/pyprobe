# coding=utf-8
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.

base = 'Console'

executables = [
    Executable('probe.py', copyDependentFiles=True)
]

includefiles = []
packages = ['pyprobe', 'psutil']
includes = []

setup(name='pyprobe',
      version='1.0',
      description='x',
      options={
          'build_exe': {
              'include_files': includefiles,
              'packages': packages,
              'excludes': [],
              'includes': ['requests']
          },
          'bdist_mac': {
              'bundle_name': 'pyprobe'
          }
      },
      executables=executables, requires=['requests', 'psutil'])
