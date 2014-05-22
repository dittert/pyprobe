#!/bin/bash

# see here... http://ghantoos.org/2008/10/19/creating-a-deb-package-from-a-python-setuppy/

BASEDIR=/tmp/pyprobe-build
APTDIR=${BASEDIR}/pyprobe-1.0

if [ -d "${BASEDIR}" ]; then
	rm -r ${BASEDIR}
	mkdir ${BASEDIR}
fi

mkdir -p ${APTDIR}/DEBIAN
cp ubuntu/control ${APTDIR}/DEBIAN/

mkdir -p ${APTDIR}/usr/local/bin
cp ubuntu/pyprobe ${APTDIR}/usr/local/bin/
chmod 555 ${APTDIR}/usr/local/bin/pyprobe

# Code bereitstellen
mkdir -p ${APTDIR}/usr/lib/python2.7/dist-packages/

# Upstart Task anlegen
mkdir -p ${APTDIR}/etc/init
cp ubuntu/pyprobe.conf ${APTDIR}/etc/init
mkdir -p ${APTDIR}/etc/init.d
ln -s /lib/init/upstart-job ${APTDIR}/etc/init.d/pyprobe 

# Verzeichnis für den Zustand
mkdir -p ${APTDIR}/run/pyprobe
chmod 750 ${APTDIR}/run/pyprobe

# Default Konfiguration
mkdir -p ${APTDIR}/etc
cp ubuntu/default-config ${APTDIR}/etc/pyprobe

cd ${BASEDIR} && dpkg-deb --build pyprobe-1.0/