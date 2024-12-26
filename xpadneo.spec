%if 0%{?fedora}
%global buildforkernels akmod
%global debug_package %{nil}
%endif

Name:     xpadneo
Version:  0.9.7
Release:  1%{?dist}
Summary:  Advanced Linux Driver for Xbox One Wireless Gamepad
Group:    System Environment/Kernel
License:  GPLv3
URL:      https://github.com/atar-axis/xpadneo
Source0:  %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:  modules-load-d-xpadneo.conf

BuildRequires:  systemd-rpm-macros

Provides:       %{name}-kmod-common = %{version}-%{release}
Requires:       %{name}-kmod >= %{version}
Obsoletes:      %{name} < 0.9.1-2

%description
Advanced Linux Driver for Xbox One Wireless Controller

%prep
%autosetup

%build
# Nothing to build

%install
install -D -m 0644 hid-xpadneo/etc-modprobe.d/xpadneo.conf %{buildroot}%{_modprobedir}/60-xpadneo.conf
install -D -m 0644 %{SOURCE1} %{buildroot}%{_modulesloaddir}/xpadneo.conf
install -D -m 0644 hid-xpadneo/etc-udev-rules.d/60-xpadneo.rules %{buildroot}%{_udevrulesdir}/60-xpadneo.rules

%files
%doc NEWS.md docs/README.md docs/CONFIGURATION.md
%license LICENSE
%{_modprobedir}/60-xpadneo.conf
%{_modulesloaddir}/xpadneo.conf
%{_udevrulesdir}/60-xpadneo.rules

%changelog
* Thu Dec 26 2024 Jan200101 <sentrycraft123@gmail.com> - 0.9.7-1
- Update to 0.9.7

* Thu Nov 28 2024 Jan200101 <sentrycraft123@gmail.com> - 0.9.6-2
- split kernel module into separate package

* Sun Jul 14 2024 Jan200101 <sentrycraft123@gmail.com> - 0.9.6-1
- Update to 0.9.6

* Wed Oct 12 2022 Jan Drögehoff <sentrycraft123@gmail.com> - 0.9.5-1
- Update to 0.9.5

* Mon Jul 04 2022 Jan Drögehoff <sentrycraft123@gmail.com> - 0.9.4-1
- Update to 0.9.4

* Sun May 29 2022 Jan Drögehoff <sentrycraft123@gmail.com> - 0.9.2-1
- Update to 0.9.2

* Thu Jun 17 2021 Jan Drögehoff <sentrycraft123@gmail.com> - 0.9.1-2
- Move from DKMS to Akmods

* Fri May 21 2021 Jan Drögehoff <sentrycraft123@gmail.com> - 0.9.1-1
- Update to 0.9.1

* Mon Dec 28 21:58:05 CET 2020 Jan Drögehoff <sentrycraft123@gmail.com> - 0.9-2
- remove configure script

* Mon Dec 28 21:01:47 CET 2020 Jan Drögehoff <sentrycraft123@gmail.com> - 0.9-1
- Initial Spec

