%if 0%{?fedora}
%global buildforkernels akmod
%endif
%global debug_package %{nil}

%global prjname xpadneo

Name:           %{prjname}-kmod
Summary:        Kernel module (kmod) for %{prjname}
Version:        0.9.8
Release:        1%{?dist}
License:        GPLv2+

URL:            https://github.com/atar-axis/xpadneo
Source0:        %{url}/archive/v%{version}/%{prjname}-%{version}.tar.gz

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  elfutils-libelf-devel
BuildRequires:  kmodtool

Requires:       bluez bluez-tools

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --kmodname %{prjname} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
Advanced Linux Driver for Xbox One Wireless Controller

This package contains the kmod module for %{prjname}.

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu} --kmodname %{prjname} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%autosetup -n %{prjname}-%{version}

for kernel_version  in %{?kernel_versions} ; do
    cp -a hid-xpadneo/src _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version  in %{?kernel_versions} ; do
  make V=1 %{?_smp_mflags} -C ${kernel_version##*___} M=${PWD}/_kmod_build_${kernel_version%%___*} VERSION=v%{version} modules
done

%install
for kernel_version in %{?kernel_versions}; do
    mkdir -p %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
    install -D -m 755 _kmod_build_${kernel_version%%___*}/hid-xpadneo.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
    chmod a+x %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/*.ko
done
%{?akmod_install}


%changelog
* Mon Jan 12 2026 Jan200101 <sentrycraft123@gmail.com> - 0.9.8-1
- Update to 0.9.8

* Thu Dec 26 2024 Jan200101 <sentrycraft123@gmail.com> - 0.9.7-1
- Update to 0.9.7

* Thu Nov 28 2024 Jan200101 <sentrycraft123@gmail.com> - 0.9.6-3
- fix pathing issue

* Thu Nov 28 2024 Jan200101 <sentrycraft123@gmail.com> - 0.9.6-2
- split kernel module into separate package

