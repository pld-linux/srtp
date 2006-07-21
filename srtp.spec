Summary:	Open-source implementation of Secure Real-time Transport Protocol
Summary(pl):	Otwarta implementacja protoko³u Secure Real-time Transport Protocol
Name:		srtp
Version:	1.4.2
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://srtp.sourceforge.net/%{name}-%{version}.tgz
# Source0-md5:	7b0ffbfad9bbaf33d397027e031cb35a
Patch0:		%{name}-shared.patch
URL:		http://srtp.sourceforge.net/srtp.html
BuildRequires:	autoconf
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The libSRTP library is an open-source implementation of Secure
Real-time Transport Protocol (SRTP).

%description -l pl
Biblioteka libSRTP to otwarta implementacja protoko³u SRTP (Secure
Real-time Transport Protocol).

%package devel
Summary:	Header files for SRTP library
Summary(pl):	Pliki nag³ówkowe biblioteki SRTP
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for SRTP library.

%description devel -l pl
Pliki nag³ówkowe biblioteki SRTP.

%package static
Summary:	Static SRTP library
Summary(pl):	Statyczna biblioteka SRTP
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static SRTP library.

%description static -l pl
Statyczna biblioteka SRTP.

%prep
%setup -q -n srtp
%patch0 -p1

%build
%{__autoconf}
%{__autoheader}
%configure
%{__make}

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
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%doc doc/{crypto_kernel.txt,intro.txt,references.txt,draft-irtf-cfrg-icm-00.txt,libsrtp.pdf}
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/srtp

%files static
%defattr(644,root,root,755)
%{_libdir}/libsrtp.a
