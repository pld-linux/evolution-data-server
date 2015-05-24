#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	kerberos5	# build without kerberos5 support
%bcond_without	ldap		# build without ldap support
%bcond_without	static_libs	# do not build static libs
%bcond_without	uoa		# single sign-on (aka Ubuntu Online Accounts)
%bcond_without	vala		# do not build Vala API

%define		basever		3.16
%define		apiver		1.2
Summary:	Evolution data server
Summary(pl.UTF-8):	Serwer danych Evolution
Name:		evolution-data-server
Version:	3.16.2
Release:	2
License:	LGPL v2+
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/evolution-data-server/3.16/%{name}-%{version}.tar.xz
# Source0-md5:	ef14158fb0486189bc4fe2a8252f6e20
URL:		http://www.gnome.org/projects/evolution/
BuildRequires:	autoconf >= 2.62
BuildRequires:	automake >= 1:1.11
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gcr-devel >= 3.4.0
BuildRequires:	gcr-ui-devel >= 3.4.0
BuildRequires:	gettext-tools >= 0.18.1
BuildRequires:	glib2-devel >= 1:2.40.0
BuildRequires:	gnome-common >= 2.20.0
BuildRequires:	gnome-online-accounts-devel >= 3.8.0
BuildRequires:	gobject-introspection-devel >= 0.10.0
BuildRequires:	gperf
BuildRequires:	gtk+3-devel >= 3.6.0
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.14}
%{?with_kerberos5:BuildRequires:	heimdal-devel}
BuildRequires:	intltool >= 0.40.0
%{?with_uoa:BuildRequires:	json-glib-devel}
%{?with_uoa:BuildRequires:	libaccounts-glib-devel >= 1.4}
BuildRequires:	libgdata-devel >= 0.15.1
BuildRequires:	libgweather-devel >= 3.8
BuildRequires:	libical-devel >= 0.43
BuildRequires:	libicu-devel
BuildRequires:	libsecret-devel >= 0.5
%{?with_uoa:BuildRequires:	libsignon-glib-devel >= 1.8}
BuildRequires:	libsoup-devel >= 2.42.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2.2
BuildRequires:	libxml2-devel >= 1:2.6.31
BuildRequires:	nspr-devel >= 4
BuildRequires:	nss-devel >= 3
%{?with_ldap:BuildRequires:	openldap-evolution-devel >= 2.4.6}
BuildRequires:	pkgconfig
%{?with_uoa:BuildRequires:	rest-devel >= 0.7}
BuildRequires:	rpmbuild(macros) >= 1.304
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite3-devel >= 3.5
BuildRequires:	tar >= 1:1.22
%{?with_vala:BuildRequires:	vala >= 2:0.22.0}
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires(post,postun):	glib2 >= 1:2.40.0
Requires:	%{name}-libs = %{version}-%{release}
Requires:	gnome-online-accounts-libs >= 3.8.0
Requires:	gtk+3 >= 3.6.0
Requires:	libgdata >= 0.15.1
Requires:	libgweather >= 3.8
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		schemadir	/usr/share/openldap/schema

%description
The Evolution data server for the calendar and addressbook.

%description -l pl.UTF-8
Serwer danych Evolution dla kalendarza i książki adresowej.

%package ldap
Summary:	LDAP support for Evolution data server
Summary(pl.UTF-8):	Obsługa LDAP dla serwera danych Evolution
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description ldap
LDAP support for Evolution data server (address book backend module).

%description ldap -l pl.UTF-8
Obsługa LDAP dla serwera danych Evolution (moduł dla książki
adresowej).

%package uoa
Summary:	Ubuntu Online Accounts support for Evolution data server
Summary(pl.UTF-8):	Obsługa Ubuntu Online Accounts dla serwera danych Evolution
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libaccounts-glib >= 1.4
Requires:	libsignon-glib >= 1.8
Requires:	rest >= 0.7

%description uoa
Ubuntu Online Accounts (single sign-on) support for Evolution data
server.

%description uoa -l pl.UTF-8
Obsługa Ubuntu Online Accounts (pojedynczego logowania) dla serwera
danych Evolution.

%package -n openldap-schema-evolutionperson
Summary:	evolutionperson LDAP schema
Summary(pl.UTF-8):	Schemat LDAP evolutionperson
Group:		Networking/Daemons
Requires(post,postun):	sed >= 4.0
Requires:	openldap-servers
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n openldap-schema-evolutionperson
This package contains evolutionperson.schema for OpenLDAP server.

%description -n openldap-schema-evolutionperson -l pl.UTF-8
Ten pakiet zawiera evolutionperson.schema dla serwera OpenLDAP.

%package libs
Summary:	Evolution Data Server library
Summary(pl.UTF-8):	Biblioteka Evolution Data Server
Group:		X11/Libraries
Requires:	gcr-libs >= 3.4.0
Requires:	gcr-ui >= 3.4.0
Requires:	glib2 >= 1:2.40.0
Requires:	libical >= 0.43
Requires:	libsecret >= 0.5
Requires:	libsoup >= 2.42.0
Requires:	libxml2 >= 1:2.6.31
Requires:	sqlite3 >= 3.5

%description libs
This package contains Evolution Data Server library.

%description libs -l pl.UTF-8
Ten pakiet zawiera bibliotekę Evolution Data Server.

%package devel
Summary:	Evolution data server development files
Summary(pl.UTF-8):	Pliki programistyczne serwera danych evolution
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	gcr-devel >= 3.4.0
Requires:	gcr-ui-devel >= 3.4.0
Requires:	glib2-devel >= 1:2.40.0
%{?with_kerberos5:Requires:	heimdal-devel}
Requires:	libgdata-devel >= 0.15.1
Requires:	libical-devel >= 0.43
Requires:	libsecret-devel >= 0.5
Requires:	libsoup-devel >= 2.42.0
Requires:	libxml2-devel >= 1:2.6.31
Requires:	nspr-devel >= 4
Requires:	nss-devel >= 3
Requires:	sqlite3-devel >= 3.5

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

%package -n vala-evolution-data-server
Summary:	Evolution data server API for Vala language
Summary(pl.UTF-8):	API serwera danych Evolution dla języka Vala
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala >= 2:0.22.0

%description -n vala-evolution-data-server
Evolution data server API for Vala language.

%description -n vala-evolution-data-server -l pl.UTF-8
API serwera danych Evolution dla języka Vala.

%prep
%setup -q

# kill -L$withval/lib
%{__sed} -i -e 's/DB_LIBS="-L[^ "]* /DB_LIBS="/;s/ICONV_LIBS="[^ "]*/ICONV_LIBS="/' configure.ac

%build
%{__gtkdocize}
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
	--enable-smime \
	--enable-ipv6 \
	%{__enable_disable apidocs gtk-doc} \
	%{__enable_disable static_libs static} \
	%{__enable_disable vala vala-bindings} \
	%{!?with_uoa:--disable-uoa} \
	--with-libdb=%{_libdir} \
	--with-html-dir=%{_gtkdocdir} \
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{name}-%{basever}
install -d $RPM_BUILD_ROOT%{schemadir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	HTML_DIR=%{_gtkdocdir}

cp -p addressbook/backends/ldap/evolutionperson.schema $RPM_BUILD_ROOT%{schemadir}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/{camel-providers,calendar-backends,addressbook-backends,credential-modules,registry-modules}/*.{la,a}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/*.{a,la}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang %{name}-%{basever}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%glib_compile_schemas

%postun
%glib_compile_schemas

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

%files -f %{name}-%{basever}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS* README
%attr(755,root,root) %{_libexecdir}/camel-index-control-%{apiver}
%attr(755,root,root) %{_libexecdir}/camel-lock-helper-%{apiver}
%attr(755,root,root) %{_libexecdir}/evolution-addressbook-factory-subprocess
%attr(755,root,root) %{_libexecdir}/evolution-addressbook-factory
%attr(755,root,root) %{_libexecdir}/evolution-calendar-factory-subprocess
%attr(755,root,root) %{_libexecdir}/evolution-calendar-factory
%attr(755,root,root) %{_libexecdir}/evolution-scan-gconf-tree-xml
%attr(755,root,root) %{_libexecdir}/evolution-source-registry
%attr(755,root,root) %{_libexecdir}/evolution-user-prompter
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/libedbus-private.so
%dir %{_libdir}/%{name}/addressbook-backends
%attr(755,root,root) %{_libdir}/%{name}/addressbook-backends/libebookbackendfile.so
%attr(755,root,root) %{_libdir}/%{name}/addressbook-backends/libebookbackendgoogle.so
%attr(755,root,root) %{_libdir}/%{name}/addressbook-backends/libebookbackendwebdav.so
%dir %{_libdir}/%{name}/calendar-backends
%attr(755,root,root) %{_libdir}/%{name}/calendar-backends/libecalbackendcaldav.so
%attr(755,root,root) %{_libdir}/%{name}/calendar-backends/libecalbackendcontacts.so
%attr(755,root,root) %{_libdir}/%{name}/calendar-backends/libecalbackendfile.so
%attr(755,root,root) %{_libdir}/%{name}/calendar-backends/libecalbackendgtasks.so
%attr(755,root,root) %{_libdir}/%{name}/calendar-backends/libecalbackendhttp.so
%attr(755,root,root) %{_libdir}/%{name}/calendar-backends/libecalbackendweather.so
%dir %{_libdir}/%{name}/camel-providers
%attr(755,root,root) %{_libdir}/%{name}/camel-providers/libcamelimapx.so
%{_libdir}/%{name}/camel-providers/libcamelimapx.urls
%attr(755,root,root) %{_libdir}/%{name}/camel-providers/libcamellocal.so
%{_libdir}/%{name}/camel-providers/libcamellocal.urls
%attr(755,root,root) %{_libdir}/%{name}/camel-providers/libcamelnntp.so
%{_libdir}/%{name}/camel-providers/libcamelnntp.urls
%attr(755,root,root) %{_libdir}/%{name}/camel-providers/libcamelpop3.so
%{_libdir}/%{name}/camel-providers/libcamelpop3.urls
%attr(755,root,root) %{_libdir}/%{name}/camel-providers/libcamelsendmail.so
%{_libdir}/%{name}/camel-providers/libcamelsendmail.urls
%attr(755,root,root) %{_libdir}/%{name}/camel-providers/libcamelsmtp.so
%{_libdir}/%{name}/camel-providers/libcamelsmtp.urls
%dir %{_libdir}/%{name}/credential-modules
%attr(755,root,root) %{_libdir}/%{name}/credential-modules/module-credentials-goa.so
%dir %{_libdir}/evolution-data-server/registry-modules
%attr(755,root,root) %{_libdir}/evolution-data-server/registry-modules/module-cache-reaper.so
%attr(755,root,root) %{_libdir}/evolution-data-server/registry-modules/module-gnome-online-accounts.so
%attr(755,root,root) %{_libdir}/evolution-data-server/registry-modules/module-google-backend.so
%attr(755,root,root) %{_libdir}/evolution-data-server/registry-modules/module-outlook-backend.so
%attr(755,root,root) %{_libdir}/evolution-data-server/registry-modules/module-owncloud-backend.so
%attr(755,root,root) %{_libdir}/evolution-data-server/registry-modules/module-secret-monitor.so
%attr(755,root,root) %{_libdir}/evolution-data-server/registry-modules/module-trust-prompt.so
%attr(755,root,root) %{_libdir}/evolution-data-server/registry-modules/module-yahoo-backend.so

%dir %{_libdir}/%{name}-%{basever}
%dir %{_datadir}/%{name}
%{_pixmapsdir}/%{name}

%{_datadir}/dbus-1/services/org.gnome.evolution.dataserver.AddressBook.service
%{_datadir}/dbus-1/services/org.gnome.evolution.dataserver.Calendar.service
%{_datadir}/dbus-1/services/org.gnome.evolution.dataserver.Sources.service
%{_datadir}/dbus-1/services/org.gnome.evolution.dataserver.UserPrompter.service

%{_datadir}/GConf/gsettings/evolution-data-server.convert
%{_datadir}/glib-2.0/schemas/org.gnome.evolution.eds-shell.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.evolution.shell.network-config.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.Evolution.DefaultSources.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.evolution-data-server.addressbook.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.evolution-data-server.calendar.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.evolution-data-server.gschema.xml

%if %{with ldap}
%files ldap
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/addressbook-backends/libebookbackendldap.so
%{_datadir}/%{name}/evolutionperson.schema
%endif

%if %{with uoa}
%files uoa
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/evolution-data-server/credential-modules/module-credentials-uoa.so
%attr(755,root,root) %{_libdir}/evolution-data-server/registry-modules/module-ubuntu-online-accounts.so
%{_desktopdir}/evolution-data-server-uoa.desktop
# XXX: which package should own these dirs?
%dir %{_datadir}/accounts
%dir %{_datadir}/accounts/applications
%{_datadir}/accounts/applications/evolution-data-server.application
%dir %{_datadir}/accounts/service_types
%{_datadir}/accounts/service_types/calendar.service-type
%{_datadir}/accounts/service_types/contacts.service-type
%{_datadir}/accounts/service_types/mail.service-type
%dir %{_datadir}/accounts/services
%{_datadir}/accounts/services/google-calendar.service
%{_datadir}/accounts/services/google-contacts.service
%{_datadir}/accounts/services/google-gmail.service
%{_datadir}/accounts/services/windows-live-mail.service
%{_datadir}/accounts/services/yahoo-calendar.service
%{_datadir}/accounts/services/yahoo-mail.service
%endif

%files -n openldap-schema-evolutionperson
%defattr(644,root,root,755)
%{schemadir}/evolutionperson.schema

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcamel-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcamel-%{apiver}.so.52
%attr(755,root,root) %{_libdir}/libebackend-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libebackend-%{apiver}.so.10
%attr(755,root,root) %{_libdir}/libebook-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libebook-%{apiver}.so.16
%attr(755,root,root) %{_libdir}/libebook-contacts-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libebook-contacts-%{apiver}.so.1
%attr(755,root,root) %{_libdir}/libecal-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libecal-%{apiver}.so.18
%attr(755,root,root) %{_libdir}/libedata-book-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libedata-book-%{apiver}.so.25
%attr(755,root,root) %{_libdir}/libedata-cal-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libedata-cal-%{apiver}.so.27
%attr(755,root,root) %{_libdir}/libedataserver-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libedataserver-%{apiver}.so.20
%attr(755,root,root) %{_libdir}/libedataserverui-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libedataserverui-%{apiver}.so.1
%{_libdir}/girepository-1.0/EBook-%{apiver}.typelib
%{_libdir}/girepository-1.0/EBookContacts-%{apiver}.typelib
%{_libdir}/girepository-1.0/EDataServer-%{apiver}.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcamel-%{apiver}.so
%attr(755,root,root) %{_libdir}/libebackend-%{apiver}.so
%attr(755,root,root) %{_libdir}/libebook-%{apiver}.so
%attr(755,root,root) %{_libdir}/libebook-contacts-%{apiver}.so
%attr(755,root,root) %{_libdir}/libecal-%{apiver}.so
%attr(755,root,root) %{_libdir}/libedata-book-%{apiver}.so
%attr(755,root,root) %{_libdir}/libedata-cal-%{apiver}.so
%attr(755,root,root) %{_libdir}/libedataserver-%{apiver}.so
%attr(755,root,root) %{_libdir}/libedataserverui-%{apiver}.so
%{_includedir}/evolution-data-server
%{_pkgconfigdir}/camel-%{apiver}.pc
%{_pkgconfigdir}/evolution-data-server-%{apiver}.pc
%{_pkgconfigdir}/libebackend-%{apiver}.pc
%{_pkgconfigdir}/libebook-%{apiver}.pc
%{_pkgconfigdir}/libebook-contacts-%{apiver}.pc
%{_pkgconfigdir}/libecal-%{apiver}.pc
%{_pkgconfigdir}/libedata-book-%{apiver}.pc
%{_pkgconfigdir}/libedata-cal-%{apiver}.pc
%{_pkgconfigdir}/libedataserver-%{apiver}.pc
%{_pkgconfigdir}/libedataserverui-%{apiver}.pc
%{_datadir}/gir-1.0/EBook-%{apiver}.gir
%{_datadir}/gir-1.0/EBookContacts-%{apiver}.gir
%{_datadir}/gir-1.0/EDataServer-%{apiver}.gir

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcamel-%{apiver}.a
%{_libdir}/libebackend-%{apiver}.a
%{_libdir}/libebook-%{apiver}.a
%{_libdir}/libebook-contacts-%{apiver}.a
%{_libdir}/libecal-%{apiver}.a
%{_libdir}/libedata-book-%{apiver}.a
%{_libdir}/libedata-cal-%{apiver}.a
%{_libdir}/libedataserver-%{apiver}.a
%{_libdir}/libedataserverui-%{apiver}.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/camel
%{_gtkdocdir}/eds
%endif

%if %{with vala}
%files -n vala-evolution-data-server
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/libebook-%{apiver}.deps
%{_datadir}/vala/vapi/libebook-%{apiver}.vapi
%{_datadir}/vala/vapi/libebook-contacts-%{apiver}.deps
%{_datadir}/vala/vapi/libebook-contacts-%{apiver}.vapi
%{_datadir}/vala/vapi/libedataserver-%{apiver}.deps
%{_datadir}/vala/vapi/libedataserver-%{apiver}.vapi
%endif
