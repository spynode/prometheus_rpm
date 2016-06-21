Name: prometheus
Version: %{getenv:RPMPACK_VER}
Release: 1%{?dist}
Summary: An open-source service monitoring system and time series database
License: Apache License 2.0
URL: http://prometheus.io
Source0: https://github.com/prometheus/prometheus/releases/download/%{version}/prometheus-%{version}.linux-amd64.tar.gz
Source1: prometheus.yml
Source2: prometheus.init
%define progdir /opt/%{name}
%define pkgname prometheus-%{version}.linux-amd64

%description

%prep
%setup -q -n %{pkgname}

%install
install -p -d %{buildroot}%{progdir}/{console_libraries,consoles,conf}
install -p -d %{buildroot}%{_initrddir}
install -p -d %{buildroot}/data/{logs,db}/%{name}
install -p -d %{buildroot}/var/run/%{name}
install -p -D -m 755 %{_builddir}/%{pkgname}/prometheus %{buildroot}%{progdir}/
install -p -D -m 755 %{_builddir}/%{pkgname}/promtool %{buildroot}%{progdir}/
install -p -D -m 644 %{_builddir}/%{pkgname}/console_libraries/* %{buildroot}%{progdir}/console_libraries/
install -p -D -m 644 %{_builddir}/%{pkgname}/consoles/* %{buildroot}%{progdir}/consoles/
install -p -D -m 644 %{S:1} %{buildroot}%{progdir}/conf/
install -p -D -m 755 %{S:2} %{buildroot}%{_initrddir}/%{name}

%files
%defattr(-,root,root,-)
%doc
%{progdir}
%{_initrddir}/%{name}
%dir %attr(-, %{name}, %{name}) /data/logs/%{name}
%dir %attr(-, %{name}, %{name}) /data/db/%{name}
%dir %attr(-, %{name}, %{name}) /var/run/%{name}

%pre
/usr/bin/getent group %{name} || /usr/sbin/groupadd -r %{name}
/usr/bin/getent passwd %{name} || /usr/sbin/useradd -g %{name} -r -M -s /bin/bash %{name}

%preun
%{_initrddir}/%{name} stop || true
