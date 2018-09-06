%global _hardened_build 1

%if 0%{?fedora}
%global with_meson 1
%endif

Name:           libvarlink
Version:        12
Release:        1%{?dist}
Summary:        Varlink C Library
License:        ASL 2.0
URL:            https://github.com/varlink/%{name}
Source0:        https://github.com/varlink/%{name}/archive/%{version}/%{name}-%{version}.tar.gz

%if !0%{?with_meson}
Patch0001:      0001-Revert-autotools-build-system-removal.patch
Patch0002:      0002-Add-aarch64-build-support.patch
%endif

%if 0%{?with_meson}
BuildRequires:  meson
%else
BuildRequires:  autoconf
BuildRequires:  automake
%endif
BuildRequires:  git
BuildRequires:  gcc

%description
Varlink C Library

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        util
Summary:        Varlink command line tools

%description    util
The %{name}-util package contains varlink command line tools.

%prep
%autosetup -S git

%build
%if 0%{?with_meson}
%meson
%meson_build
%else
./autogen.sh
%configure
%make_build
%endif

%check
export LC_CTYPE=C.utf8
%if 0%{?with_meson}
%meson_test
%else
# FIXME(hguemar): lib/test-symbols.sh fails on ppc64le
%ifnarch %{power64}
make check
%endif
%endif

%install
%if 0%{?with_meson}
%meson_install
%else
%make_install
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license LICENSE
%{_libdir}/libvarlink.so.*

%files util
%{_bindir}/varlink
%{_datadir}/bash-completion/completions/varlink
%{_datadir}/vim/vimfiles/after/*

%files devel
%{_includedir}/varlink.h
%{_libdir}/libvarlink.so
%{_libdir}/pkgconfig/libvarlink.pc

%changelog
* Mon Sep  3 2018 Haïkel Guémar <hguemar@fedoraproject.org> - 12-1
- Initial packaging for RDO

