# NOTE: for srtp 2.x see libsrtp2.spec
Summary:	Open-source implementation of Secure Real-time Transport Protocol
Summary(pl.UTF-8):	Otwarta implementacja protokołu Secure Real-time Transport Protocol
Name:		srtp
Version:	1.6.0
Release:	2
License:	BSD
Group:		Libraries
Source0:	https://github.com/cisco/libsrtp/archive/v%{version}/libsrtp-%{version}.tar.gz
# Source0-md5:	0f2188e50468a52cdd51d0479849236a
Patch0:		%{name}-rename_functions.patch
Patch1:		%{name}-headers.patch
Patch2:		%{name}-ismacryp.patch
URL:		https://github.com/cisco/libsrtp
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libpcap-devel
BuildRequires:	openssl-devel >= 1.0.1
BuildRequires:	pkgconfig
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
Requires:	libpcap-devel
Requires:	openssl-devel >= 1.0.1
Requires:	zlib-devel

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
%setup -q -n libsrtp-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%configure \
	--enable-openssl

%{__make} shared_library
%{__make} all

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES LICENSE README TODO
%attr(755,root,root) %{_libdir}/libsrtp.so.1

%files devel
%defattr(644,root,root,755)
%doc doc/{*.txt,*.pdf}
%attr(755,root,root) %{_libdir}/libsrtp.so
%{_pkgconfigdir}/libsrtp.pc
%{_includedir}/srtp

%files static
%defattr(644,root,root,755)
%{_libdir}/libsrtp.a
