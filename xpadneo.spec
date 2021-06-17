%if 0%{?fedora}
%global buildforkernels akmod
%global debug_package %{nil}
%endif

Name:     xpadneo
Version:  0.9.1
Release:  2%{?dist}
Summary:  Advanced Linux Driver for Xbox One Wireless Gamepad
Group:    System Environment/Kernel
License:  GPLv3
URL:      https://github.com/atar-axis/xpadneo
Source0:  %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

%global   srcname hid-%{name}

BuildRequires:  make
BuildRequires:  help2man
BuildRequires:  gcc
BuildRequires:  kmodtool

Requires:       bash
Requires:       bluez bluez-tools
Requires:       %{name}-kmod = %{version}

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu}--kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
Advanced Linux Driver for Xbox One Wireless Controller

%package kmod
Summary:  Kernel module (kmod) for %{name}
Requires: kernel-devel

%description kmod
This is the first driver for the Xbox One Wireless Gamepad (which is shipped with the Xbox One S).

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q

for kernel_version  in %{?kernel_versions} ; do
  cp -a . _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version  in %{?kernel_versions} ; do
  make V=1 %{?_smp_mflags} -C ${kernel_version##*___} M=${PWD}/_kmod_build_${kernel_version%%___*} modules
done

%install
for kernel_version in %{?kernel_versions}; do
 mkdir -p %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
 install -D -m 755 _kmod_build_${kernel_version%%___*}/v4l2loopback.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
 chmod a+x %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/*.ko
done
%{?akmod_install}

%files
%doc NEWS.md docs/README.md docs/CONFIGURATION.md
%license LICENSE

%changelog
* Thu Jun 17 2021 Jan Drögehoff <sentrycraft123@gmail.com> - 0.9.1-2
- Move from DKMS to Akmods

* Fri May 21 2021 Jan Drögehoff <sentrycraft123@gmail.com> - 0.9.1-1
- Update to 0.9.1

* Mon Dec 28 21:58:05 CET 2020 Jan Drögehoff <sentrycraft123@gmail.com> - 0.9-2
- remove configure script

* Mon Dec 28 21:01:47 CET 2020 Jan Drögehoff <sentrycraft123@gmail.com> - 0.9-1
- Initial Spec

