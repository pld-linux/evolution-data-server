#
# todo:
# - system libical
#
# Conditional build:
%bcond_without	kerberos5	# build without kerberos5 support
%bcond_without	ldap		# build without ldap support
#
%define		basever		1.6
%define		apiver		1.2
Summary:	Evolution data server
Summary(pl.UTF-8):	Serwer danych Evolution
Name:		evolution-data-server
Version:	1.6.3
Release:	5
License:	GPL
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/evolution-data-server/1.6/%{name}-%{version}.tar.bz2
# Source0-md5:	e40343fa6a80916da3f4d1ba5d118c89
Patch0:		%{name}-system_db.patch
Patch1:		%{name}-GG-IM.patch
Patch2:		%{name}-workaround-cal-backend-leak.patch
Patch3:		%{name}-gcc4.patch
Patch4:		%{name}-ac.patch
URL:		http://www.ximian.com/products/ximian_evolution/
BuildRequires:	ORBit2-devel >= 1:2.14.0
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	db-devel
BuildRequires:	gnome-common >= 2.8.0
%{?with_kerberos5:BuildRequires:	heimdal-devel >= 0.7}
BuildRequires:	intltool
BuildRequires:	libglade2-devel >= 1:2.5.1
BuildRequires:	libgnomeui-devel >= 2.14.1
BuildRequires:	libsoup-devel >= 2.2.93
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	nspr-devel
BuildRequires:	nss-devel
%{?with_ldap:BuildRequires:	openldap-devel >= 2.3.0}
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.304
Requires(post,postun):	scrollkeeper
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		schemadir	/usr/share/openldap/schema

%description
The Evolution data server for the calendar and addressbook.

%description -l pl.UTF-8
Serwer danych Evolution dla kalendarza i książki adresowej.

%package -n openldap-schema-evolutionperson
Summary:	evolutionperson LDAP schema
Summary(pl.UTF-8):	Schemat LDAP evolutionperson
Group:		Networking/Daemons
Requires(post,postun):	sed >= 4.0
Requires:	openldap-servers

%description -n openldap-schema-evolutionperson
This package contains evolutionperson.schema for openldap server.

%description -n openldap-schema-evolutionperson -l pl.UTF-8
Ten pakiet zawiera evolutionperson.schema dla serwera openldap.

%package libs
Summary:	Evolution Data Server library
Summary(pl.UTF-8):	Biblioteka Evolution Data Server
Group:		X11/Libraries
Requires:	libgnomeui >= 2.14.1
Requires:	libsoup >= 2.2.93

%description libs
This package contains Evolution Data Server library.

%description libs -l pl.UTF-8
Ten pakiet zawiera bibliotekę Evolution Data Server.

%package devel
Summary:	Evolution data server development files
Summary(pl.UTF-8):	Pliki programistyczne serwera danych evolution
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
%{?with_kerberos5:Requires:	heimdal-devel >= 0.7}
# for all but libegroupwise
Requires:	GConf2-devel >= 2.14.0
Requires:	ORBit2-devel >= 1:2.14.0
Requires:	glib2-devel >= 1:2.6.4
Requires:	libbonobo-devel >= 2.14.0
Requires:	libgnomeui-devel >= 2.14.0
Requires:	libxml2-devel
# for libegroupwise
Requires:	libsoup-devel >= 2.2.93

%description devel
This package contains the files necessary to develop applications
using Evolution's data server libraries.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki potrzebne do tworzenia aplikacji
korzystających z bibliotek serwera danych Evolution.

%package static
Summary:	Evolution data server static libraries
Summary(pl.UTF-8):	Statyczne biblioteki serwera danych Evolution
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Evolution data server static libraries.

%description static -l pl.UTF-8
Statyczne biblioteki serwera danych Evolution.

%package apidocs
Summary:	e-d-s API documentation
Summary(pl.UTF-8):	Dokumentacja API e-d-s
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
e-d-s API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API e-d-s.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

rm -rf libdb

%build
%{__glib_gettextize}
%{__intltoolize}
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
	%{?with_kerberos5:--with-krb5=%{_prefix}} \
	%{!?with_kerberos5:--with-krb5=no} \
	%{?with_ldap:--with-openldap=yes} \
	%{!?with_ldap:--with-openldap=no} \
	--enable-gtk-doc \
	--enable-static \
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

rm $RPM_BUILD_ROOT%{_libdir}/%{name}-%{apiver}/{camel-providers,extensions}/*.{la,a}

rm -r $RPM_BUILD_ROOT%{_datadir}/locale/no

install -d $RPM_BUILD_ROOT%{schemadir}
install addressbook/backends/ldap/evolutionperson.schema $RPM_BUILD_ROOT%{schemadir}

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%scrollkeeper_update_post

%postun
%scrollkeeper_update_postun

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post -n openldap-schema-evolutionperson
%openldap_schema_register %{schemadir}/evolutionperson.schema
%service -q ldap restart

%postun -n openldap-schema-evolutionperson
if [ "$1" = "0" ]; then
	%openldap_schema_unregister %{schemadir}/evolutionperson.schema
	%service -q ldap restart
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS* README
%attr(755,root,root) %{_libdir}/camel-index-control-%{apiver}
%attr(755,root,root) %{_libdir}/camel-lock-helper-%{apiver}
%attr(755,root,root) %{_libdir}/evolution-data-server-%{basever}
%dir %{_libdir}/%{name}-%{apiver}
%dir %{_libdir}/%{name}-%{apiver}/camel-providers
%attr(755,root,root) %{_libdir}/%{name}-%{apiver}/camel-providers/*.so
%{_libdir}/%{name}-%{apiver}/camel-providers/*.urls
%dir %{_libdir}/%{name}-%{apiver}/extensions
%attr(755,root,root) %{_libdir}/%{name}-%{apiver}/extensions/*.so
%{_libdir}/bonobo/servers/GNOME_Evolution_DataServer_1.2.server

%if %{with ldap}
%{_datadir}/%{name}-%{basever}/*.schema
%endif

%dir %{_datadir}/%{name}-%{basever}
%{_datadir}/%{name}-%{basever}/glade
%{_datadir}/%{name}-%{basever}/weather
%{_datadir}/%{name}-%{basever}/zoneinfo
%{_pixmapsdir}/%{name}-%{basever}

%files -n openldap-schema-evolutionperson
%defattr(644,root,root,755)
%{schemadir}/evolutionperson.schema

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcamel-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcamel-%{apiver}.so.0
%attr(755,root,root) %{_libdir}/libcamel-provider-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcamel-provider-%{apiver}.so.8
%attr(755,root,root) %{_libdir}/libebook-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libebook-%{apiver}.so.5
%attr(755,root,root) %{_libdir}/libecal-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libecal-%{apiver}.so.6
%attr(755,root,root) %{_libdir}/libedata-book-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libedata-book-%{apiver}.so.2
%attr(755,root,root) %{_libdir}/libedata-cal-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libedata-cal-%{apiver}.so.5
%attr(755,root,root) %{_libdir}/libedataserver-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libedataserver-%{apiver}.so.7
%attr(755,root,root) %{_libdir}/libedataserverui-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libedataserverui-%{apiver}.so.6
%attr(755,root,root) %{_libdir}/libegroupwise-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libegroupwise-%{apiver}.so.10
%attr(755,root,root) %{_libdir}/libexchange-storage-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libexchange-storage-%{apiver}.so.1
%{_datadir}/idl/%{name}-%{apiver}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcamel-%{apiver}.so
%attr(755,root,root) %{_libdir}/libcamel-provider-%{apiver}.so
%attr(755,root,root) %{_libdir}/libebook-%{apiver}.so
%attr(755,root,root) %{_libdir}/libecal-%{apiver}.so
%attr(755,root,root) %{_libdir}/libedata-book-%{apiver}.so
%attr(755,root,root) %{_libdir}/libedata-cal-%{apiver}.so
%attr(755,root,root) %{_libdir}/libedataserver-%{apiver}.so
%attr(755,root,root) %{_libdir}/libedataserverui-%{apiver}.so
%attr(755,root,root) %{_libdir}/libegroupwise-%{apiver}.so
%attr(755,root,root) %{_libdir}/libexchange-storage-%{apiver}.so
%{_libdir}/libcamel-%{apiver}.la
%{_libdir}/libcamel-provider-%{apiver}.la
%{_libdir}/libebook-%{apiver}.la
%{_libdir}/libecal-%{apiver}.la
%{_libdir}/libedata-book-%{apiver}.la
%{_libdir}/libedata-cal-%{apiver}.la
%{_libdir}/libedataserver-%{apiver}.la
%{_libdir}/libedataserverui-%{apiver}.la
%{_libdir}/libegroupwise-%{apiver}.la
%{_libdir}/libexchange-storage-%{apiver}.la
%{_includedir}/evolution-data-server-%{basever}
%{_pkgconfigdir}/camel-%{apiver}.pc
%{_pkgconfigdir}/camel-provider-%{apiver}.pc
%{_pkgconfigdir}/evolution-data-server-%{apiver}.pc
%{_pkgconfigdir}/libebook-%{apiver}.pc
%{_pkgconfigdir}/libecal-%{apiver}.pc
%{_pkgconfigdir}/libedata-book-%{apiver}.pc
%{_pkgconfigdir}/libedata-cal-%{apiver}.pc
%{_pkgconfigdir}/libedataserver-%{apiver}.pc
%{_pkgconfigdir}/libedataserverui-%{apiver}.pc
%{_pkgconfigdir}/libegroupwise-%{apiver}.pc
%{_pkgconfigdir}/libexchange-storage-%{apiver}.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libcamel-%{apiver}.a
%{_libdir}/libcamel-provider-%{apiver}.a
%{_libdir}/libebook-%{apiver}.a
%{_libdir}/libecal-%{apiver}.a
%{_libdir}/libedata-book-%{apiver}.a
%{_libdir}/libedata-cal-%{apiver}.a
%{_libdir}/libedataserver-%{apiver}.a
%{_libdir}/libedataserverui-%{apiver}.a
%{_libdir}/libegroupwise-%{apiver}.a
%{_libdir}/libexchange-storage-%{apiver}.a

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libebook
%{_gtkdocdir}/libecal
%{_gtkdocdir}/libedata-cal
%{_gtkdocdir}/libedataserver
