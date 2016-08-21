# centos-rpm-odr-dabmux
CentOS 7 RPM Specfile for [Opendigitalradio's ODR-DabMux](https://github.com/Opendigitalradio/ODR-DabMux) which is part of [RaBe's DAB / DAB+ broadcasting package collection](https://build.opensuse.org/project/show/home:radiorabe:dab).

## Usage
There are pre-built binary packages for CentOS 7 available on [Radio RaBe's OBS DAB / DAB+ broadcasting package repository](https://build.opensuse.org/project/show/home:radiorabe:dab), which can be installed as follows:

```bash
curl -o /etc/yum.repos.d/home:radiorabe:dab.repo \
     http://download.opensuse.org/repositories/home:/radiorabe:/dab/CentOS_7/home:radiorabe:dab.repo
     
yum install odr-dabmux
