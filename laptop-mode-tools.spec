Summary: Tools for power savings based on battery/AC status
Name: laptop-mode-tools
Version: 1.62
Release: 1%{?dist}

License: GPLv2
Group: System Environment/Base
URL: http://www.samwel.tk/laptop_mode

Source: http://www.samwel.tk/laptop_mode/tools/downloads/laptop-mode-tools_%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch

%description
Laptop mode is a Linux kernel feature that allows your laptop to save
considerable power, by allowing the hard drive to spin down for longer
periods of time. This package contains the userland scripts that are
needed to enable laptop mode. It includes support for automatically
enabling laptop mode when the computer is working on batteries. In
addition, it provides a set of modules which allow you to apply
various other power savings.

%prep
%setup -n %{name}_%{version}

%build

%{__rm} -rf %{buildroot}

DESTDIR=%{buildroot} INIT_D="" MAN_D=%{_mandir} INSTALL=install ./install.sh

find %{buildroot}%{_mandir} -type f -exec chmod 644 {} \;
find %{buildroot}%{_mandir} -type f -exec gzip {} \;

%clean
%{__rm} -rf %{buildroot}

%preun
if [ $1 -eq 0 ]; then
	/sbin/service laptop-mode stop &>/dev/null || :
	/sbin/chkconfig --del laptop-mode
fi

%post
/sbin/chkconfig --add laptop-mode
/sbin/service laptop-mode start &>/dev/null || :
/sbin/service acpid restart &>/dev/null || :

%postun
/sbin/service laptop-mode condrestart &>/dev/null || :

%files
%defattr(-, root, root, 0755)

%doc COPYING Documentation/*.txt README
%{_mandir}/man8/*
%{_sysconfdir}/acpi/actions/lm_*.sh
%config(noreplace) %{_sysconfdir}/acpi/events/lm_*
%config %{_sysconfdir}/udev/rules.d/99-laptop-mode.rules
%config(noreplace) %{_sysconfdir}/laptop-mode/conf.d/*.conf
%config(noreplace) %{_sysconfdir}/laptop-mode/*.conf
%{_sysconfdir}/init.d/laptop-mode
/lib/udev/lmt-udev
/lib/systemd/system/laptop-mode.service

%{_sysconfdir}/apm/event.d/*
%{_sysconfdir}/power/scripts.d/*
%{_sysconfdir}/power/event.d/*
%{_sbindir}/*
%{_datadir}/laptop-mode-tools/*
%{_usr}/lib/pm-utils/sleep.d/*
%{_usr}/lib/tmpfiles.d/laptop-mode.conf


%changelog
* Tue Jan 22 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 1.62-1.R
- initial build
