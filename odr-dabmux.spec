#
# spec file for package odr-dabmux
#
# Copyright (c) 2016 - 2018 Radio Bern RaBe
#                           http://www.rabe.ch
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public 
# License as published  by the Free Software Foundation, version
# 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License  along with this program.
# If not, see <http://www.gnu.org/licenses/>.
#
# Please submit enhancements, bugfixes or comments via GitHub:
# https://github.com/radiorabe/centos-rpm-odr-dabmux
#

# Name of the GitHub repository
%define reponame ODR-DabMux

Name:           odr-dabmux
Version:        1.3.3
Release:        1%{?dist}
Summary:        ODR-DabMux is a DAB (Digital Audio Broadcasting) multiplexer.

License:        GPLv3+
URL:            https://github.com/Opendigitalradio/%{reponame}
Source0:        https://github.com/Opendigitalradio/%{reponame}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        odr-dabmux.service

BuildRequires:  boost-devel
BuildRequires:  libcurl-devel
BuildRequires:  systemd
BuildRequires:  zeromq-devel
Requires:       boost
Requires:       libcurl
Requires:       shadow-utils
Requires:       zeromq
%{?systemd_requires}

%description
ODR-DabMux is a DAB (Digital Audio Broadcasting) multiplexer compliant to ETSI
EN 300 401. It is the continuation of the work started by the Communications
Research Center Canada on CRC-DabMux, and is now pursued in the
Opendigitalradio project.


%prep
%setup -q -n %{reponame}-%{version}


%build
autoreconf -fi
%configure --disable-static

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%make_install

# Install the systemd service unit
install -d %{buildroot}/%{_unitdir}
install %{SOURCE1} %{buildroot}/%{_unitdir}

# Rename the README.md to prevent a name clash with the top-level README.md
mv doc/README.md doc/README-ODR-DabMux.md

# Move the man page to its proper location
mkdir -p %{buildroot}%{_mandir}/man1
mv doc/DabMux.1 %{buildroot}%{_mandir}/man1/

# Install system directories
install -d %{buildroot}/%{_sysconfdir}/%{name}


%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -d /dev/null -m -s /sbin/nologin \
    -c "%{name} system user account" %{name}
exit 0


%post
%systemd_post %{name}.service


%preun
%systemd_preun %{name}.service


%postun
%systemd_postun_with_restart %{name}.service


%files
%doc ChangeLog README.md doc/*.txt doc/README-ODR-DabMux.md doc/*.mux
%dir %{_sysconfdir}/%{name}
%{_bindir}/*
%{_mandir}/man1/*
%{_unitdir}/%{name}.service



%changelog
* Sat Feb 10 2018 Christian Affolter <c.affolter@purplehaze.ch> - 1.3.3-1
- Version bump to 1.3.3

* Tue Aug 22 2017 Christian Affolter <c.affolter@purplehaze.ch> - 1.3.0-1
- Version bump to 1.3.0

* Fri Feb 03 2017 Christian Affolter <c.affolter@purplehaze.ch> - 1.2.1-1
- Version bump to 1.2.1

* Fri Jan 27 2017 Christian Affolter <c.affolter@purplehaze.ch> - 1.2.0-1
- Version bump to 1.2.0, removed libfec dependency which is bundled now

* Sat Sep  3 2016 Lucas Bickel <hairmare@rabe.ch> - 1.1.0-1
- Version bump

* Sat Aug 27 2016 Christian Affolter <c.affolter@purplehaze.ch> - 1.0.0-2
- Added a dedicated system user and a systemd service unit for starting odr-dabmux
  based on the original work done by Lucas Bickel <hairmare@rabe.ch>

* Sun Aug 21 2016 Christian Affolter <c.affolter@purplehaze.ch> - 1.0.0-1
- Initial release
