%global	  debug_package %{nil}

Name:     xpadneo
Version:  0.9
Release:  2%{?dist}
Summary:  Advanced Linux Driver for Xbox One Wireless Gamepad
Group:    System Environment/Kernel
License:  GPLv3
URL:      https://github.com/atar-axis/xpadneo
Source0:  %{url}/archive/v%{version}.tar.gz

%global   srcname hid-%{name}

BuildArch: noarch

BuildRequires:  make
BuildRequires:  help2man

Requires:       bash
Requires:       bluez bluez-tools
Requires:       %{name}-kmod = %{version}

%description
Advanced Linux Driver for Xbox One Wireless Controller

%package dkms
Summary:  Kernel module to create Video4Linux loopback devices (DKMS)
Requires: dkms >= 2.2
Requires: kernel-devel
Provides: %{name}-kmod = %{version}

%description dkms
This package contains the module source and DKMS configuration to build the
xpadneo kernel module.

%post dkms
%{_prefix}/lib/dkms/common.postinst %{srcname} %{version}

%preun dkms
if [ $1 -ne 1 ]; then
    dkms remove -m %{srcname} -v %{version} --all --rpm_safe_upgrade || :
fi

%prep
%setup -q

cd hid-%{name}
sed -i 's/"@DO_NOT_CHANGE@"/"'"%{version}"'"/g' dkms.conf src/version.h

%install
%{__rm} -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_usrsrc}
mkdir -p %{buildroot}%{_bindir}

cp -r hid-xpadneo %{buildroot}%{_usrsrc}/%{srcname}-%{version}

%files
%doc NEWS.md docs/README.md docs/CONFIGURATION.md
%license LICENSE

%files dkms
%{_usrsrc}/hid-%{name}-%{version}

%changelog
* Mon Dec 28 21:58:05 CET 2020 Jan Drögehoff <sentrycraft123@gmail.com> - 0.9-2
- remove configure script

* Mon Dec 28 21:01:47 CET 2020 Jan Drögehoff <sentrycraft123@gmail.com> - 0.9-1
- Initial Spec

