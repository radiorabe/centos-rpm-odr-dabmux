#
# spec file for package odr-dabmux
#
# Copyright (c) 2016 Radio Bern RaBe
#                    http://www.rabe.ch
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
Version:        1.0.0
Release:        1%{?dist}
Summary:        ODR-DabMux is a DAB (Digital Audio Broadcasting) multiplexer.

License:        GPLv3+
URL:            https://github.com/Opendigitalradio/%{reponame}
Source0:        https://github.com/Opendigitalradio/%{reponame}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        odr-dabmux.service

BuildRequires:  boost-devel
BuildRequires:  libcurl-devel
BuildRequires:  libfec-odr-devel
BuildRequires:  zeromq-devel
Requires:       boost
Requires:       libcurl
Requires:       libfec-odr
Requires:       shadow-utils
Requires:       zeromq

%description
ODR-DabMux is a DAB (Digital Audio Broadcasting) multiplexer compliant to
ETSI EN 300 401. It is the continuation of the work started by the
Communications Research Center Canada on CRC-DabMux, and is now pursued in the
Opendigitalradio project.


%prep
%setup -q -n %{reponame}-%{version}
cp %SOURCE1 .


%build
autoreconf -fi
%configure --disable-static \
           --enable-input-zeromq \
           --enable-output-zeromq

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%make_install

# Install the systemd configuration
install -d %{buildroot}/%{_libdir}/systemd/system
install odr-dabmux.service %{buildroot}/%{_libdir}/systemd/system/

# Rename the README.md to prevent a name clash with the top-level README.md
mv doc/README.md doc/README-ODR-DabMux.md

# Move the man page to it's proper location
mkdir -p %{buildroot}%{_mandir}/man1
mv doc/DabMux.1 %{buildroot}%{_mandir}/man1/

# Install system directories
install -d %{buildroot}/%{_sysconfdir}/%{name}
install -d %{buildroot}/%{_sharedstatedir}/%{name}


%pre
getent group odr-dabmux >/dev/null || groupadd -r odr-dabmux
getent passwd odr-dabmux >/dev/null || \
    useradd -r -g odr-dabmux -d /var/lib/odr-dabmux -m -s /sbin/nologin \
    -c "odr-dabmux system user account" odr-dabmux
exit 0


%files
%doc ChangeLog README.md doc/*.txt doc/README-ODR-DabMux.md doc/*.mux
%dir %{_sysconfdir}/%{name}
%dir %attr(-, odr-dabmux, odr-dabmux) %{_sharedstatedir}/%{name}
%{_bindir}/*
%{_mandir}/man1/*
%{_libdir}/systemd/system/*



%changelog
* Sun Aug 21 2016 Christian Affolter <c.affolter@purplehaze.ch> - 1.0.0-1
- Initial release

