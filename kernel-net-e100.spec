# conditional build
# _without_dist_kernel          without distribution kernel
%define		_orig_name	e100

Summary:	Intel(R) PRO/100 driver for Linux
Summary(pl):	Sterownik do karty Intel(R) PRO/100
Name:		kernel-net-%{_orig_name}
Version:	2.1.24
%define	_rel	1
Release:	%{_rel}@%{_kernel_ver_str}
License:	BSD
Vendor:		Intel Corporation
Group:		Base/Kernel
Source0:	ftp://aiedownload.intel.com/df-support/2896/eng/%{_orig_name}-%{version}.tar.gz
URL:		http://support.intel.com/support/network/adapter/pro100/
%{!?_without_dist_kernel:BuildRequires:         kernel-source > 2.4 }
BuildRequires:	%{kgcc_package}
Prereq:		/sbin/depmod
%{!?_without_dist_kernel:%requires_releq_kernel_up}
Provides:	kernel(e100)
Obsoletes:	e100
Obsoletes:	linux-net-e100
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the Linux driver for the Intel(R) PRO/100 family
of 10/100 Ethernet network adapters.

%description -l pl
Ten pakiet zawiera sterownik dla Linuksa do kart sieciowych 10/100Mbit
z rodziny Intel(R) PRO/100.

%package -n kernel-smp-net-%{_orig_name}
Summary:	Intel(R) PRO/100 driver for Linux SMP
Summary(pl):	Sterownik do karty Intel(R) PRO/100
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Prereq:		/sbin/depmod
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
Obsoletes:	e100
Obsoletes:	linux-net-e100
Provides:	kernel(e100)

%description -n kernel-smp-net-%{_orig_name}
This package contains the Linux SMP driver for the Intel(R) PRO/100
family of 10/100 Ethernet network adapters.

%description -n kernel-smp-net-%{_orig_name} -l pl
Ten pakiet zawiera sterownik dla Linuksa SMP do kart sieciowych
10/100Mbit z rodziny Intel(R) PRO/100.

%prep
%setup -q -n %{_orig_name}-%{version}

%build
%{__make} -C src SMP=1 CC="%{kgcc} -DCONFIG_X86_LOCAL_APIC -DSTB_WA" KSRC=%{_kernelsrcdir}
mv -f src/%{_orig_name}.o src/%{_orig_name}-smp.o
%{__make} -C src clean KSRC=%{_kernelsrcdir}
%{__make} -C src CC="%{kgcc} -DSTB_WA" KSRC=%{_kernelsrcdir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc
install src/%{_orig_name}-smp.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/%{_orig_name}.o
install src/%{_orig_name}.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/%{_orig_name}.o

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
%doc e100.7 README LICENSE
/lib/modules/%{_kernel_ver}/misc/*

%files -n kernel-smp-net-%{_orig_name}
%defattr(644,root,root,755)
%doc e100.7 README LICENSE
/lib/modules/%{_kernel_ver}smp/misc/*
