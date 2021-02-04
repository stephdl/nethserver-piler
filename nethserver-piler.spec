Summary: nethserver-piler  is a skeleton for a new module
%define name nethserver-piler
Name: %{name}
%define version 0.1.0
%define release 1
Version: %{version}
Release: %{release}%{?dist}
License: GPL
Group: Networking/Daemons
Source: %{name}-%{version}.tar.gz
%define composeVersion 1.28.2
Source1: https://github.com/docker/compose/releases/download/%{composeVersion}/docker-compose-Linux-x86_64
Requires: nethserver-docker
Requires: nethserver-mail-server
BuildRequires: nethserver-devtools
BuildArch: x86_64

%description
skeleton for a new module



%prep
mv %SOURCE1 %SOURCE1-%{composeVersion}
%setup

%build
# %{makedocs}
perl createlinks

%install



rm -rf $RPM_BUILD_ROOT
(cd root   ; find . -depth -print | cpio -dump $RPM_BUILD_ROOT)
rm -f %{name}-%{version}-%{release}-filelist
# Temp directory
# cd ../
mkdir -p %{buildroot}/usr/share/piler/
# mkdir -p %{buildroot}/var/lib/docker/volumes/piler_piler_etc/_data/

# install -d -m 755 %{buildroot}%{_datadir}/%{version}.tar.gz
mv %SOURCE1-%{composeVersion} %{buildroot}%{_datadir}/piler/docker-compose

%{genfilelist} $RPM_BUILD_ROOT \
> %{name}-%{version}-%{release}-filelist

%post
%postun

%clean 
rm -rf $RPM_BUILD_ROOT
rm -rf  %SOURCE1-%{composeVersion}

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)
%dir %{_nseventsdir}/%{name}-update
# %dir %attr(0755,root,root) /var/lib/docker/volumes/piler_piler_etc/_data/
%attr(0755,root,root) /usr/share/piler/docker-compose
%attr(0755,root,root) /usr/libexec/nethserver/piler-docker-management
%doc COPYING

%changelog
* Tue May 09 2017 stephane de Labrusse <stephdl@de-labrusse.fr>
- initial
