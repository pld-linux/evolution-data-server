#
# Conditional build:
%bcond_without	kerberos5	# build without kerberos5 support
%bcond_without	ldap		# build without ldap support
#
%define		basever		2.32
%define		apiver		1.2
Summary:	Evolution data server
Summary(pl.UTF-8):	Serwer danych Evolution
Name:		evolution-data-server
Version:	2.32.2
Release:	3
License:	LGPL v2+
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/evolution-data-server/2.32/%{name}-%{version}.tar.bz2
# Source0-md5:	19d230667c0dfb1c06b8fe951fd552ff
Patch0:		gtk224.patch
URL:		http://www.gnome.org/projects/evolution/
BuildRequires:	GConf2-devel >= 2.26.0
BuildRequires:	ORBit2-devel >= 1:2.14.8
BuildRequires:	autoconf >= 2.58
BuildRequires:	automake >= 1:1.10
BuildRequires:	bison
BuildRequires:	cyrus-sasl-devel
BuildRequires:	db-devel
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.26.0
BuildRequires:	gnome-common >= 2.20.0
BuildRequires:	gperf
BuildRequires:	gtk+2-devel >= 2:2.16.0
BuildRequires:	gtk-doc >= 1.9
%{?with_kerberos5:BuildRequires:	heimdal-devel}
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libgdata-devel >= 1:0.6.3
BuildRequires:	libgnome-keyring-devel >= 2.26.0
BuildRequires:	libgweather-devel >= 2.26.0
BuildRequires:	libical-devel >= 0.43
BuildRequires:	libsoup-devel >= 2.26.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 1:2.6.31
BuildRequires:	nspr-devel
BuildRequires:	nss-devel
%{?with_ldap:BuildRequires:	openldap-evolution-devel >= 2.4.6}
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.304
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite3-devel >= 3.5
BuildRequires:	zlib-devel
Requires:	%{name}-libs = %{version}-%{release}
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
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
Requires:	libsoup >= 2.26.0

%description libs
This package contains Evolution Data Server library.

%description libs -l pl.UTF-8
Ten pakiet zawiera bibliotekę Evolution Data Server.

%package devel
Summary:	Evolution data server development files
Summary(pl.UTF-8):	Pliki programistyczne serwera danych evolution
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	GConf2-devel >= 2.26.0
Requires:	ORBit2-devel >= 1:2.14.8
Requires:	glib2-devel >= 1:2.26.0
Requires:	gtk+2-devel >= 2:2.16.0
%{?with_kerberos5:Requires:	heimdal-devel}
Requires:	libgdata-devel >= 1:0.6.3
Requires:	libical-devel >= 0.43
Requires:	libsoup-devel >= 2.26.0
Requires:	libxml2-devel >= 1:2.6.31
Requires:	nspr-devel
Requires:	nss-devel
Requires:	sqlite3-devel

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
Summary:	Evolution data server API documentation
Summary(pl.UTF-8):	Dokumentacja API serwera danych Evolution
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
Evolution data server API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API serwera danych Evolution.

%prep
%setup -q
%patch0 -p1

# kill -L$withval/lib
sed -i -e 's/DB_LIBS="-L[^ "]* /DB_LIBS="/;s/ICONV_LIBS="[^ "]*/ICONV_LIBS="/' configure.ac

%build
%{__gtkdocize}
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoheader}
%{__autoconf}
%{__automake}

# Set LIBS so that configure will be able to link with static LDAP libraries,
# which depend on Cyrus SASL and OpenSSL.
if pkg-config openssl ; then
	LIBS="-lsasl2 `pkg-config --libs openssl`"
else
	LIBS="-lsasl2 -lssl -lcrypto"
fi
export LIBS

%configure \
	%{?with_kerberos5:--with-krb5=%{_prefix} --with-krb5-libs=%{_libdir}} \
	%{!?with_kerberos5:--with-krb5=no} \
	%{?with_ldap:--with-openldap=%{_libdir}/evolution-openldap} \
	%{?with_ldap:--with-static-ldap=yes} \
	%{!?with_ldap:--with-openldap=no} \
	--enable-gnome-keyring=yes \
	--enable-gtk-doc \
	--enable-static \
	--with-libdb=%{_libdir} \
	--with-html-dir=%{_gtkdocdir} \
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{schemadir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	HTML_DIR=%{_gtkdocdir}

install addressbook/backends/ldap/evolutionperson.schema $RPM_BUILD_ROOT%{schemadir}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}-%{apiver}/{camel-providers,extensions}/*.{la,a}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

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
%attr(755,root,root) %{_libdir}/e-addressbook-factory
%attr(755,root,root) %{_libdir}/e-calendar-factory
%dir %{_libdir}/%{name}-%{apiver}
%dir %{_libdir}/%{name}-%{apiver}/camel-providers
%attr(755,root,root) %{_libdir}/%{name}-%{apiver}/camel-providers/*.so
%{_libdir}/%{name}-%{apiver}/camel-providers/*.urls
%dir %{_libdir}/%{name}-%{apiver}/extensions
%attr(755,root,root) %{_libdir}/%{name}-%{apiver}/extensions/*.so

%if %{with ldap}
%{_datadir}/%{name}-%{basever}/*.schema
%endif

%{_datadir}/dbus-1/services/org.gnome.evolution.dataserver.AddressBook.service
%{_datadir}/dbus-1/services/org.gnome.evolution.dataserver.Calendar.service

%dir %{_datadir}/%{name}-%{basever}
%{_datadir}/%{name}-%{basever}/ui
%{_datadir}/%{name}-%{basever}/weather
%{_pixmapsdir}/%{name}

%files -n openldap-schema-evolutionperson
%defattr(644,root,root,755)
%{schemadir}/evolutionperson.schema

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcamel-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcamel-%{apiver}.so.19
%attr(755,root,root) %{_libdir}/libcamel-provider-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcamel-provider-%{apiver}.so.19
%attr(755,root,root) %{_libdir}/libebackend-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libebackend-%{apiver}.so.0
%attr(755,root,root) %{_libdir}/libebook-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libebook-%{apiver}.so.10
%attr(755,root,root) %{_libdir}/libecal-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libecal-%{apiver}.so.8
%attr(755,root,root) %{_libdir}/libedata-book-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libedata-book-%{apiver}.so.8
%attr(755,root,root) %{_libdir}/libedata-cal-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libedata-cal-%{apiver}.so.10
%attr(755,root,root) %{_libdir}/libedataserver-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libedataserver-%{apiver}.so.14
%attr(755,root,root) %{_libdir}/libedataserverui-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libedataserverui-%{apiver}.so.11
%attr(755,root,root) %{_libdir}/libegroupwise-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libegroupwise-%{apiver}.so.13

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcamel-%{apiver}.so
%attr(755,root,root) %{_libdir}/libcamel-provider-%{apiver}.so
%attr(755,root,root) %{_libdir}/libebackend-%{apiver}.so
%attr(755,root,root) %{_libdir}/libebook-%{apiver}.so
%attr(755,root,root) %{_libdir}/libecal-%{apiver}.so
%attr(755,root,root) %{_libdir}/libedata-book-%{apiver}.so
%attr(755,root,root) %{_libdir}/libedata-cal-%{apiver}.so
%attr(755,root,root) %{_libdir}/libedataserver-%{apiver}.so
%attr(755,root,root) %{_libdir}/libedataserverui-%{apiver}.so
%attr(755,root,root) %{_libdir}/libegroupwise-%{apiver}.so
%{_includedir}/evolution-data-server-%{basever}
%{_pkgconfigdir}/camel-%{apiver}.pc
%{_pkgconfigdir}/camel-provider-%{apiver}.pc
%{_pkgconfigdir}/evolution-data-server-%{apiver}.pc
%{_pkgconfigdir}/libebackend-%{apiver}.pc
%{_pkgconfigdir}/libebook-%{apiver}.pc
%{_pkgconfigdir}/libecal-%{apiver}.pc
%{_pkgconfigdir}/libedata-book-%{apiver}.pc
%{_pkgconfigdir}/libedata-cal-%{apiver}.pc
%{_pkgconfigdir}/libedataserver-%{apiver}.pc
%{_pkgconfigdir}/libedataserverui-%{apiver}.pc
%{_pkgconfigdir}/libegroupwise-%{apiver}.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libcamel-%{apiver}.a
%{_libdir}/libcamel-provider-%{apiver}.a
%{_libdir}/libebackend-%{apiver}.a
%{_libdir}/libebook-%{apiver}.a
%{_libdir}/libecal-%{apiver}.a
%{_libdir}/libedata-book-%{apiver}.a
%{_libdir}/libedata-cal-%{apiver}.a
%{_libdir}/libedataserver-%{apiver}.a
%{_libdir}/libedataserverui-%{apiver}.a
%{_libdir}/libegroupwise-%{apiver}.a

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/camel
%{_gtkdocdir}/libebackend
%{_gtkdocdir}/libebook
%{_gtkdocdir}/libecal
%{_gtkdocdir}/libedata-book
%{_gtkdocdir}/libedata-cal
%{_gtkdocdir}/libedataserver
%{_gtkdocdir}/libedataserverui
