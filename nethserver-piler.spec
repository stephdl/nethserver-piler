Summary: nethserver-piler  is a rpm for mailpiler software
%define name nethserver-piler
Name: %{name}
%define version 0.1.1
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
sed -i 's/_RELEASE_/%{version}/' %{name}.json

%install
rm -rf $RPM_BUILD_ROOT
(cd root   ; find . -depth -print | cpio -dump $RPM_BUILD_ROOT)

mkdir -p %{buildroot}/usr/share/cockpit/%{name}/
mkdir -p %{buildroot}/usr/share/cockpit/nethserver/applications/
mkdir -p %{buildroot}/usr/libexec/nethserver/api/%{name}/
cp -a manifest.json %{buildroot}/usr/share/cockpit/%{name}/
cp -a logo.png %{buildroot}/usr/share/cockpit/%{name}/
cp -a %{name}.json %{buildroot}/usr/share/cockpit/nethserver/applications/
cp -a api/* %{buildroot}/usr/libexec/nethserver/api/%{name}/

rm -f %{name}-%{version}-%{release}-filelist
mkdir -p %{buildroot}/usr/share/piler/
mv %SOURCE1 %{buildroot}%{_datadir}/piler/docker-compose

%{genfilelist} $RPM_BUILD_ROOT \
> %{name}-%{version}-%{release}-filelist

%post
getent group piler >/dev/null || groupadd -r piler
if ! id piler >/dev/null 2>&1 ; then
    useradd -r -g piler piler
fi

%postun
if [ $1 == 0 ] ; then
    /usr/bin/rm -f /etc/httpd/conf.d/zzz_piler.conf
    /usr/bin/systemctl reload httpd
fi

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
* Tue Feb 16 2021 stephane de Labrusse <stephdl@de-labrusse.fr>
- First release only imap authentication is supported

* Sat Feb 06 2021 stephane de Labrusse <stephdl@de-labrusse.fr>
- initial
- Fosdem 21 I miss you
