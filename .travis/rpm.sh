#!/bin/bash
#
# RPM build wrapper for odr-dabmux, runs inside the build container on travis-ci

set -xe

curl -o /etc/yum.repos.d/dab.repo https://download.opensuse.org/repositories/home:/radiorabe:/dab/CentOS_7/home:radiorabe:dab.repo

yum -y install \
    epel-release

chown root:root odr-dabmux.spec

rpmdev-setuptree

cp *.service /root/rpmbuild/SOURCES/

build-rpm-package.sh odr-dabmux.spec
