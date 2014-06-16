pyprobe
=======

pyprobe allows you to monitor your Linux systems from PRTG. It is an implementation of the PRTG MiniProbe API written
in Python 2.7. The current release runs on Ubuntu 12.04 LTS (Precise) and 14.04 LTS (Trusty Tahr). 


sensors
-------
Currently, the following sensor types are supported:

* Ping: Monitors hosts through ping
* CPU Load: Monitors CPU load per core
* CPU Temperature: Monitors the temperature of the CPU per core 
* Memory Info: Monitors memory usage
* Swap File Usage: Monitors the usage of the swap file
* Drive Capacity: Monitors the amount of free space of a drive
* IO Load: monitors the IO load of a drive
* Uptime: Monitors the uptime of a system
* S.M.A.R.T.: Monitors a hard drive based on its S.M.A.R.T. values. Requires smartmontools to be installed.

It is possible to run the MiniProbe on OS X as well, although there is no installation package for OS X at the moment.
The following OS X specific sensors are implemented right now: 

* Promise Pegasus RAID Array: Monitors a Promise Pegasus RAID array.
* Promise Pegasus Drive: Monitors a drive of a Promise Pegasus RAID array based on its S.M.A.R.T. values
* Promise Pegasus Enclosure: Monitors a Promise Pegasus R6 drive enclosure
* Apple Software RAID: Monitors the state of an Apple Software RAID drive

All sensors messages are in German at the moment. Let me know if you're intersted in an English version.

Installation and Requirements
-----------------------------

There are prebuilt available for Ubuntu 12.04 LTS, 13.10 and 14.04 LTS. The installation process is still being worked 
on. In the mean time, here are some simple steps to install on Ubuntu:

 * Download the .deb file (see locations below). For example: `wget http://pyprobe.24objects.de/precise/python-pyprobe_1.0_all.deb`
 * `sudo dpkg -i python-pyprobe_1.0_all.deb`
 * Edit the configuration file in /etc/pyprobe. You need to provide the key to access the server (Configuration >
   Server & Probes) and the hostname of the server
 * `initctl start python-pyprobe`

Distribution | Download Link
------------ | --------------------------------------------------------------
12.04 LTS    | http://pyprobe.24objects.de/precise/python-pyprobe_1.0_all.deb
13.10        | http://pyprobe.24objects.de/saucy/python-pyprobe_1.0_all.deb
14.04 LTS    | http://pyprobe.24objects.de/trusty/python-pyprobe_1.0_all.deb

Some sensors require additional packages to be installed. You can install them with your local package manager. For 
example `apt-get install smartmontools` installs the dependencies for the S.M.A.R.T. sensor.

Sensor            | Dependency
----------------- | -------
CPU temperature   | lm-sensors
S.M.A.R.T. values | smartmontools


A few words about OS X
----------------------
Currently, there are no prepackaged packages for OS X. Current versions of OS X already come with Python 2.7 
preinstalled. However, you can clone the Github repository and use setuptools to install the MiniProbe. If you want the 
probe to start as a daemon on system startup, you'll need to create the appropriate configuration files for launchd. 
Contributions for OS X are welcome!