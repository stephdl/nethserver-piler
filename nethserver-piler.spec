Summary: nethserver-piler  is a rpm for mailpiler software
%define name nethserver-piler
Name: %{name}
%define version 0.1.0
%define release 1
Version: %{version}
Release: %{release}%{?dist}
License: GPL
Group: Networking/Daemons
Source: %{name}-%{version}.tar.gz
# rm docker-compose-Linux-x86_64 for version upgrade
%define composeVersion 1.28.2
Source1: https://github.com/docker/compose/releases/download/%{composeVersion}/docker-compose-Linux-x86_64
Requires: nethserver-docker
Requires: nethserver-mail-server
BuildRequires: nethserver-devtools
BuildArch: x86_64

%description
Piler is a feature rich open source email archiving solution

%prep
%setup

%build
perl createlinks

%install
rm -rf $RPM_BUILD_ROOT
(cd root   ; find . -depth -print | cpio -dump $RPM_BUILD_ROOT)
rm -f %{name}-%{version}-%{release}-filelist
mkdir -p %{buildroot}/usr/share/piler/
mv %SOURCE1 %{buildroot}%{_datadir}/piler/docker-compose

%{genfilelist} $RPM_BUILD_ROOT \
> %{name}-%{version}-%{release}-filelist

%post
%postun

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)
%dir %{_nseventsdir}/%{name}-update
%attr(0755,root,root) /usr/share/piler/docker-compose
%attr(0755,root,root) /usr/libexec/nethserver/nethserver-piler-docker-management
%attr(0755,root,root) /usr/libexec/nethserver/nethserver-piler-expand-template
%attr(0755,root,root) /usr/bin/piler
%attr(0755,root,root) /usr/bin/piler-import-email
%doc COPYING

%changelog
* Sat fev 06 2021 stephane de Labrusse <stephdl@de-labrusse.fr>
- initial
- Fosdem 21 I miss you
