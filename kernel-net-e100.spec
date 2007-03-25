#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel

%define		_orig_name	e100

Summary:	Intel(R) PRO/100 driver for Linux
Summary(pl.UTF-8):	Sterownik do karty Intel(R) PRO/100
Name:		kernel-net-%{_orig_name}
Version:	3.5.17
%define	_rel	1
Release:	%{_rel}@%{_kernel_ver_str}
License:	BSD
Vendor:		Intel Corporation
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/e1000/%{_orig_name}-%{version}.tar.gz
# Source0-md5:	519bc00c3315e127530dbe6968358634
URL:		http://support.intel.com/support/network/adapter/pro100/
BuildRequires:	rpmbuild(macros) >= 1.379
%{?with_dist_kernel:%requires_releq_kernel}
Requires(post,postun):	/sbin/depmod
Provides:	kernel(e100)
Obsoletes:	e100
Obsoletes:	linux-net-e100
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the Linux driver for the Intel(R) PRO/100 family
of 10/100 Ethernet network adapters.

%description -l pl.UTF-8
Ten pakiet zawiera sterownik dla Linuksa do kart sieciowych 10/100Mbit
z rodziny Intel(R) PRO/100.

%prep
%setup -q -n %{_orig_name}-%{version}
cat > src/Makefile <<'EOF'
obj-m := e100.o
e100-objs := ethtool.o
EOF

%build
%build_kernel_modules -C src -m e100

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -m src/e100 -d kernel/drivers/net/misc -n e100 -s current

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%files
%defattr(644,root,root,755)
%doc e100.7 README LICENSE
/etc/modprobe.d/%{_kernel_ver}/e100.conf
/lib/modules/%{_kernel_ver}/kernel/drivers/net/misc/e100*.ko*
