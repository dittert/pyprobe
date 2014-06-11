pyprobe
=======

pyprobe is a PRTG Mini Probe implemented in Python 2.7. It currently supports Linux and OS X systems.

Many sensors require the probe to be installed on the machine that should be monitored. This caused by the fact that
the sensors require direct access to hardware devices.

sensors
-------
Currently, the following sensor types are supported:

* Ping: Monitors hosts through ping
* CPU Load: Monitors CPU load per core
* Memory Info: Monitors memory usage
* Swap File Usage: Monitors the usage of the swap file
* Drive Capacity: Monitors the amount of free space on drive
* IO Load: monitors the IO load of a device
* Uptime: Monitors the uptime of a system
* S.M.A.R.T.: Monitors a hard drive based on its S.M.A.R.T. values. Requires smartmontools to be installed.

OS X specific sensors:

* Promise Pegasus RAID Array: Monitors a Promise Pegasus RAID array.
* Promise Pegasus Drive: Monitors a drive of a Promise Pegasus RAID array based on its S.M.A.R.T. values
* Promise Pegasus Enclosure: Monitors a Promise Pegasus R6 drive enclosure
* Apple Software RAID: Monitors the state of an Apple Software RAID drive


Installation and Requirements
=============================

OS X
----
Python 2.7 is included in OS X 10.8 and 10.9.

An installation of smartmontools is required if you're planning on monitoring S.M.A.R.T. values. The easiest way to
install smartmontools is through Home Brew or MacPorts. Make sure that you set the correct path to smartctl
in the configuration file.

There is no prepackaged version at the moment but will be available later.

Ubuntu
------
I am still working on the installation process of the probe. A full ppa with signed .deb files will be available later.

**Although the probe is running quite well, it is not yet ready for production use. Packaging for Debian/Ubuntu 
isn't fully done yet. User at your own risk!**

Please perform the following steps to install the probe on Ubuntu 12.04:
 
 * wget http://pyprobe.24objects.de/python-pyprobe_1.0_all.deb
 * sudo dpkg -i python-pyprobe_1.0_all.deb
 * Edit the configuration file in /etc/pyprobe. You need to provide the key to access the server (Configuration >
   Server & Probes) and the hostname of the server
 * sudo service python-pyprobe start

An installation of smartmontools is required if you're planning on monitoring S.M.A.R.T. values. You can install this
dependency with the package manager of your system. Make sure that you set the correct path to smartctl in the
configuration file.
