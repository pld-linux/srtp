#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries

%define		rel	4
%define		subver	20121108
Summary:	Open-source implementation of Secure Real-time Transport Protocol
Summary(pl.UTF-8):	Otwarta implementacja protokołu Secure Real-time Transport Protocol
Name:		srtp
Version:	1.4.4
Release:	%{rel}.%{subver}
License:	BSD
Group:		Libraries
# Source0:	http://srtp.sourceforge.net/%{name}-%{version}.tgz
# Upstream 1.4.4 tarball is a bit dated, need to use cvs
# cvs -d:pserver:anonymous@srtp.cvs.sourceforge.net:/cvsroot/srtp co -P srtp
# tar cvfj srtp-1.4.4-20101004cvs.tar.bz2 srtp/
Source0:	http://dev.gentoo.org/~phajdan.jr/%{name}-%{version}_p%{subver}.tar.gz
# Source0-md5:	1d1a644d3847000b8e186578867bf839
Source1:	lib%{name}.pc
Patch0:		%{name}-shared.patch
Patch1:		%{name}-rename_functions.patch
URL:		http://srtp.sourceforge.net/srtp.html
BuildRequires:	autoconf
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fPIC

%description
The libSRTP library is an open-source implementation of Secure
Real-time Transport Protocol (SRTP).

%description -l pl.UTF-8
Biblioteka libSRTP to otwarta implementacja protokołu SRTP (Secure
Real-time Transport Protocol).

%package devel
Summary:	Header files for SRTP library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki SRTP
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for SRTP library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki SRTP.

%package static
Summary:	Static SRTP library
Summary(pl.UTF-8):	Statyczna biblioteka SRTP
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static SRTP library.

%description static -l pl.UTF-8
Statyczna biblioteka SRTP.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1

%build
%{__autoconf}
%{__autoheader}
%configure \
	%{?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

/sbin/ldconfig -n $RPM_BUILD_ROOT%{_libdir}
ln -sf $(basename $RPM_BUILD_ROOT%{_libdir}/libsrtp.so.*.*.*) $RPM_BUILD_ROOT%{_libdir}/libsrtp.so

# Install the pkg-config file
install -d $RPM_BUILD_ROOT%{_pkgconfigdir}
sed -e "
	s|@PREFIX@|%{_prefix}|g
	s|@LIBDIR@|%{_libdir}|g
	s|@INCLUDEDIR@|%{_includedir}|g
" < %{SOURCE1} > $RPM_BUILD_ROOT%{_pkgconfigdir}/libsrtp.pc

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES LICENSE README TODO
%attr(755,root,root) %{_libdir}/libsrtp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsrtp.so.0

%files devel
%defattr(644,root,root,755)
%doc doc/{crypto_kernel.txt,intro.txt,references.txt,draft-irtf-cfrg-icm-00.txt,libsrtp.pdf}
%attr(755,root,root) %{_libdir}/libsrtp.so
%{_pkgconfigdir}/libsrtp.pc
%{_libdir}/libsrtp.la
%{_includedir}/srtp

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libsrtp.a
%endif
