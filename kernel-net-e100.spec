
# conditional build
# _without_dist_kernel          without distribution kernel

%define		_kernel_ver	%(grep UTS_RELEASE %{_kernelsrcdir}/include/linux/version.h 2>/dev/null | cut -d'"' -f2)
%define		_kernel_ver_str	%(echo %{_kernel_ver} | sed s/-/_/g)
%define		_orig_name	e100
%define		_rel 3

Summary:	Intel(R) PRO/100 driver for Linux
Summary(pl):	Sterownik do karty Intel(R) PRO/100
Name:		kernel-net-%{_orig_name}
Version:	1.6.29
Release:	%{_rel}@%{_kernel_ver_str}
License:	BSD
Vendor:         Intel Corporation
Group:		Base/Kernel
Group(de):	Grundsätzlich/Kern
Group(pl):	Podstawowe/J±dro
Source0:	ftp://aiedownload.intel.com/df-support/2896/eng/%{_orig_name}-%{version}.tar.gz
Patch0:		%{_orig_name}-makefile.patch
Patch1:		%{_orig_name}-redefine.patch
%{!?_without_dist_kernel:BuildRequires:         kernel-headers }
Obsoletes: 	kernel-smp-net-%{_orig_name}
Obsoletes:      e100
Obsoletes:      linux-net-e100
Provides:       kernel(e100)
Prereq:		/sbin/depmod
%{!?_without_dist_kernel:Conflicts:	kernel < %{_kernel_ver}, kernel > %{_kernel_ver}}
%{!?_without_dist_kernel:Conflicts:	kernel-smp}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the Linux driver for the Intel(R) PRO/100 family
of 10/100 Ethernet network adapters.

%description -l pl
Ten pakiet zawiera sterownik dla Linuksa do kart sieciowych 10/100Mbit
z rodziny Intel(R) PRO/100.


%package -n kernel-smp-net-%{_orig_name}
Summary:        Intel(R) PRO/100 driver for Linux SMP
Summary(pl):    Sterownik do karty Intel(R) PRO/100
Release:        %{_rel}@%{_kernel_ver_str}
%{!?_without_dist_kernel:Conflicts:     kernel < %{_kernel_ver}, kernel > %{_kernel_ver}}
%{!?_without_dist_kernel:Conflicts:     kernel-up}
Obsoletes: 	kernel-net-%{_orig_name}
Obsoletes:      e100
Obsoletes:      linux-net-e100
Provides:       kernel(e100)
Group:		Base/Kernel
Group(de):	Grundsätzlich/Kern
Group(pl):	Podstawowe/J±dro

%description -n kernel-smp-net-%{_orig_name}
This package contains the Linux SMP driver for the Intel(R) PRO/100 family
of 10/100 Ethernet network adapters.

%description -n kernel-smp-net-%{_orig_name} -l pl
Ten pakiet zawiera sterownik dla Linuksa SMP do kart sieciowych 10/100Mbit
z rodziny Intel(R) PRO/100.

%prep
%setup -q -n e100-%{version}
%patch0 -p0
%patch1 -p0

%build
%{__make} -C src SMP=1 CC="kgcc -DCONFIG_X86_LOCAL_APIC -DSTB_WA"
mv src/%{_orig_name}.o src/%{_orig_name}-smp.o
%{__make} -C src clean
%{__make} -C src CC="kgcc -DSTB_WA"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/net
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/net
install src/%{_orig_name}-smp.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/net/%{_orig_name}.o
install src/%{_orig_name}.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/net/%{_orig_name}.o

gzip -9nf %{_orig_name}.txt

%clean 
rm -rf $RPM_BUILD_ROOT

%post
/sbin/depmod -a

%postun
/sbin/depmod -a

%post -n kernel-smp-net-%{_orig_name}
/sbin/depmod -a

%postun -n kernel-smp-net-%{_orig_name}
/sbin/depmod -a

%files
%defattr(644,root,root,755)
%doc *.gz
/lib/modules/%{_kernel_ver}/net/*

%files -n kernel-smp-net-%{_orig_name}
%defattr(644,root,root,755)
%doc *.gz 
/lib/modules/%{_kernel_ver}smp/net/*
