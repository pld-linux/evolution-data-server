Summary:	Evolution data server
Name:		evolution-data-server
Version:	0.0.3
Release:	0.1
License:	GPL
Group:		Libraries
Source0:	ftp://ftp.gnome.org/pub/gnome/sources/evolution-data-server/0.0/%{name}-%{version}.tar.gz
# Source0-md5:	bcacfd623db973a100deb67f0b7d8a38
URL:		http://www.gnome.org
BuildRequires:	libsoup-devel >= 2.1.2
Requires(post):	/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Evolution data server.

%package devel
Summary:	Evolution data server development files
Group:		Development/Libraries

%description devel
Evolution data server development files.

%description devel -l pl

%package static
Summary:	Evolution data server static libraries
Group:		Development/Libraries

%description static
Evolution data server static libraries.

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CREDITS ChangeLog NEWS README THANKS TODO

%files devel
%defattr(644,root,root,755)

%files static
%defattr(644,root,root,755)
