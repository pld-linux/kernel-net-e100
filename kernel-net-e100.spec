#
# Conditional build:
# _without_dist_kernel          without distribution kernel
#
%define		_orig_name	e100


%{!?_without_dist_kernel:%define        _mod_name %{_orig_name}_intel }
%{?_without_dist_kernel:%define         _mod_name %{_orig_name} }

Summary:	Intel(R) PRO/100 driver for Linux
Summary(pl):	Sterownik do karty Intel(R) PRO/100
Name:		kernel-net-%{_orig_name}
Version:	3.3.6
%define	_rel	0.1
Release:	%{_rel}@%{_kernel_ver_str}
License:	BSD
Vendor:		Intel Corporation
Group:		Base/Kernel
Source0:	ftp://aiedownload.intel.com/df-support/2896/eng/%{_orig_name}-%{version}.tar.gz
# Source0-md5:	6f4fb4e4092c65c59fc560803d1da4ab
URL:		http://support.intel.com/support/network/adapter/pro100/
%{!?_without_dist_kernel:BuildRequires:	kernel-source > 2.4 }
BuildRequires:	%{kgcc_package}
BuildRequires:	rpmbuild(macros) >= 1.118
%{!?_without_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
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
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
Provides:	kernel(e100)
Obsoletes:	e100
Obsoletes:	linux-net-e100

%description -n kernel-smp-net-%{_orig_name}
This package contains the Linux SMP driver for the Intel(R) PRO/100
family of 10/100 Ethernet network adapters.

%description -n kernel-smp-net-%{_orig_name} -l pl
Ten pakiet zawiera sterownik dla Linuksa SMP do kart sieciowych
10/100Mbit z rodziny Intel(R) PRO/100.

%prep
%setup -q -n %{_orig_name}-%{version}

%build
%ifarch %{ix86}
%{__make} -C src SMP=1 CC="%{kgcc} -DCONFIG_X86_LOCAL_APIC -DSTB_WA" KSRC=%{_kernelsrcdir}
%endif
%ifarch ppc
%{__make} -C src SMP=1 CC="%{kgcc} -msoft-float  -DSTB_WA" KSRC=%{_kernelsrcdir}
%endif
%ifnarch %{ix86} ppc
%{__make} -C src SMP=1 CC="%{kgcc} -DSTB_WA" KSRC=%{_kernelsrcdir}
%endif
mv -f src/%{_orig_name}.o src/%{_orig_name}-smp.o

%{__make} -C src clean KSRC=%{_kernelsrcdir}

%ifarch ppc
%{__make} -C src CC="%{kgcc} -msoft-float -DSTB_WA" KSRC=%{_kernelsrcdir}
%else
%{__make} -C src CC="%{kgcc} -DSTB_WA" KSRC=%{_kernelsrcdir}
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/net/misc
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/misc
install src/%{_orig_name}-smp.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/misc/%{_mod_name}.o
install src/%{_orig_name}.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/net/misc/%{_mod_name}.o

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%post	-n kernel-smp-net-%{_orig_name}
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-net-%{_orig_name}
%depmod %{_kernel_ver}smp

%files
%defattr(644,root,root,755)
%doc e100.7 README LICENSE
/lib/modules/%{_kernel_ver}/kernel/drivers/net/misc/*

%files -n kernel-smp-net-%{_orig_name}
%defattr(644,root,root,755)
%doc e100.7 README LICENSE
/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/misc/*
