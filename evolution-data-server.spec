#
# todo:
# - system libical
#
%define		mver		1.2

Summary:	Evolution data server
Summary(pl):	Serwer danych Evolution
Name:		evolution-data-server
Version:	1.1.5
Release:	1
License:	GPL
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/%{name}/1.1/%{name}-%{version}.tar.bz2
# Source0-md5:	42bae6c8458c9bd1bcecc16570d43e81
Patch0:		%{name}-system_db.patch
Patch1:		%{name}-GG-IM.patch
Patch2:		%{name}-workaround-cal-backend-leak.patch
URL:		http://www.ximian.com/products/ximian_evolution/
BuildRequires:	ORBit2-devel >= 1:2.12.1
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	db-devel
BuildRequires:	gnome-common >= 2.8.0
BuildRequires:	intltool
BuildRequires:	libglade2-devel >= 1:2.5.0
BuildRequires:	libgnomeui-devel >= 2.9.1
BuildRequires:	libsoup-devel >= 2.2.2
BuildRequires:	libtool
BuildRequires:	nspr-devel
Buildrequires:	nss-devel
BuildRequires:	openldap-devel
BuildRequires:	pkgconfig
Requires(post,postun):	/sbin/ldconfig
Requires(post,postun):	/usr/bin/scrollkeeper-update
Requires(post):		GConf2
Requires:	libsoup >= 2.2.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Evolution data server for the calendar and addressbook.

%description -l pl
Serwer danych Evolution dla kalendarza i ksi±¿ki adresowej.

%package devel
Summary:	Evolution data server development files
Summary(pl):	Pliki programistyczne serwera danych evolution
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
# for all but libegroupwise
Requires:	GConf2-devel >= 2.9.2
Requires:	ORBit2-devel >= 1:2.12.1
Requires:	glib2-devel >= 1:2.6.2
Requires:	libbonobo-devel >= 2.8.1
Requires:	libgnome-devel >= 2.9.1
Requires:	libxml2-devel
# for libegroupwise
Requires:	libsoup-devel >= 2.2.2

%description devel
This package contains the files necessary to develop applications
using Evolution's data server libraries.

%description devel -l pl
Ten pakiet zawiera pliki potrzebne do tworzenia aplikacji
korzystaj±cych z bibliotek serwera danych Evolution.

%package static
Summary:	Evolution data server static libraries
Summary(pl):	Statyczne biblioteki serwera danych Evolution
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Evolution data server static libraries.

%description static -l pl
Statyczne biblioteki serwera danych Evolution.

%prep
%setup -q 
%patch0 -p1
%patch1 -p1
%patch2 -p1

rm -rf libdb

%build
glib-gettextize --copy --force
intltoolize --copy --force
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}

cd calendar/libical
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
cd ../..

%configure \
	--enable-gtk-doc \
	--enable-static \
	--with-openldap=yes \
	--with-nspr-includes=%{_includedir}/nspr \
	--with-nspr-libs=%{_libdir} \
	--with-nss-includes=%{_includedir}/nss \
	--with-nss-libs=%{_libdir}

%{__make} \
	HTML_DIR=%{_gtkdocdir} \
	GTKHTML_DATADIR=%{_datadir}/idl 

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	GTKHTML_DATADIR=%{_datadir}/idl \
	HTML_DIR=%{_gtkdocdir} \
	pkgconfigdir=%{_pkgconfigdir}

rm -r $RPM_BUILD_ROOT%{_datadir}/locale/no

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
/usr/bin/scrollkeeper-update
%gconf_schema_install

%postun
/sbin/ldconfig
/usr/bin/scrollkeeper-update

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS* README
%attr(755,root,root) %{_libdir}/%{name}-%{mver}
%attr(755,root,root) %{_libdir}/camel-index-control-%{mver}
%attr(755,root,root) %{_libdir}/camel-lock-helper-%{mver}
%attr(755,root,root) %{_libdir}/*.so.*.*
%{_libdir}/bonobo/servers/*
%{_datadir}/idl/*
%dir %{_datadir}/%{name}-%{mver}
%{_datadir}/%{name}-%{mver}/glade
%{_datadir}/%{name}-%{mver}/weather
%{_datadir}/%{name}-%{mver}/zoneinfo
%{_datadir}/%{name}-%{mver}/*.schema
%{_pixmapsdir}/%{name}-%{mver}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/*
%{_pkgconfigdir}/*
%{_gtkdocdir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
