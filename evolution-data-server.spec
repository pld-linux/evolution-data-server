#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	kerberos5	# Kerberos5 support
%bcond_without	ldap		# LDAP support
%bcond_without	goa		# Gnome Online Accounts support
%bcond_without	phonenumber	# libphonenumber support for address books
%bcond_without	vala		# Vala API

%define		apiver		1.2
%define		cal_apiver	2.0
%define		ui4_apiver	1.0
Summary:	Evolution data server
Summary(pl.UTF-8):	Serwer danych Evolution
Name:		evolution-data-server
Version:	3.56.2
Release:	2
License:	LGPL v2+
Group:		X11/Libraries
Source0:	https://download.gnome.org/sources/evolution-data-server/3.56/%{name}-%{version}.tar.xz
# Source0-md5:	e946e30d6d458fa67f63cec1d3b15212
Patch0:		%{name}-gtkdoc.patch
URL:		https://gitlab.gnome.org/GNOME/evolution/-/wikis/home
BuildRequires:	cmake >= 3.15
BuildRequires:	db-devel
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-tools >= 0.18.1
BuildRequires:	glib2-devel >= 1:2.68
%{?with_goa:BuildRequires:	gnome-online-accounts-devel >= 3.8.0}
BuildRequires:	gobject-introspection-devel >= 0.10.0
BuildRequires:	gperf
BuildRequires:	gtk+3-devel >= 3.20
BuildRequires:	gtk4-devel >= 4.4
BuildRequires:	gtk-webkit4.1-devel >= 2.34.0
BuildRequires:	gtk-webkit6-devel >= 2.40.0
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.14}
%{?with_kerberos5:BuildRequires:	heimdal-devel}
BuildRequires:	intltool >= 0.40.0
BuildRequires:	json-glib-devel >= 1.0.4
BuildRequires:	libcanberra-gtk3-devel >= 0.25
%{?with_kerberos5:BuildRequires:	libcom_err-devel}
BuildRequires:	libgdata-devel >= 0.15.1
# libgweather4 built with libsoup3
BuildRequires:	libgweather4-devel >= 4
BuildRequires:	libical-glib-devel >= 3.0.7
BuildRequires:	libicu-devel
%{?with_phonenumber:BuildRequires:	libphonenumber-devel}
BuildRequires:	libsecret-devel >= 0.5
BuildRequires:	libsoup3-devel >= 3.1.1
BuildRequires:	libstdc++-devel >= 6:5.0
BuildRequires:	libtool >= 2:2.2
BuildRequires:	libuuid-devel >= 2.0
BuildRequires:	libxml2-devel >= 1:2.6.31
BuildRequires:	nspr-devel >= 4
BuildRequires:	nss-devel >= 3
%{?with_ldap:BuildRequires:	openldap-devel >= 2.4.6}
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	sqlite3-devel >= 3.7.17
BuildRequires:	tar >= 1:1.22
%{?with_vala:BuildRequires:	vala >= 2:0.22.0}
BuildRequires:	vala-libical-glib >= 3.0.7
BuildRequires:	vala-libgdata >= 0.15.1
%{?with_goa:BuildRequires:	vala-gnome-online-accounts >= 3.8.0}
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires(post,postun):	glib2 >= 1:2.68
Requires:	%{name}-gtk3-libs = %{version}-%{release}
Requires:	%{name}-libs = %{version}-%{release}
%{?with_goa:Requires:	gnome-online-accounts-libs >= 3.8.0}
Requires:	gtk+3 >= 3.20
Requires:	gtk4 >= 4.4
Requires:	libgdata >= 0.15.1
Requires:	libgweather4 >= 4
Obsoletes:	evolution-data-server-uoa < 3.32
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

%package -n openldap-schema-evolutionperson
Summary:	evolutionperson LDAP schema
Summary(pl.UTF-8):	Schemat LDAP evolutionperson
Group:		Networking/Daemons
Requires(post,postun):	sed >= 4.0
Requires:	openldap-servers
BuildArch:	noarch

%description -n openldap-schema-evolutionperson
This package contains evolutionperson.schema for OpenLDAP server.

%description -n openldap-schema-evolutionperson -l pl.UTF-8
Ten pakiet zawiera evolutionperson.schema dla serwera OpenLDAP.

%package libs
Summary:	Evolution Data Server library
Summary(pl.UTF-8):	Biblioteka Evolution Data Server
Group:		X11/Libraries
Requires:	glib2 >= 1:2.68
Requires:	gtk4 >= 4.4
Requires:	gtk-webkit6 >= 2.40.0
Requires:	json-glib >= 1.0.4
Requires:	libical-glib >= 3.0.7
Requires:	libsecret >= 0.5
Requires:	libsoup3 >= 3.1.1
Requires:	libxml2 >= 1:2.6.31
Requires:	sqlite3 >= 3.7.17
Obsoletes:	evolution-data-server-static < 3.24

%description libs
This package contains Evolution Data Server library.

%description libs -l pl.UTF-8
Ten pakiet zawiera bibliotekę Evolution Data Server.

%package devel
Summary:	Evolution data server development files
Summary(pl.UTF-8):	Pliki programistyczne serwera danych evolution
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.68
Requires:	gtk4-devel >= 4.4
%{?with_kerberos5:Requires:	heimdal-devel}
Requires:	libgdata-devel >= 0.15.1
Requires:	libical-glib-devel >= 3.0.7
Requires:	libsecret-devel >= 0.5
Requires:	libsoup3-devel >= 3.1.1
Requires:	libxml2-devel >= 1:2.6.31
Requires:	nspr-devel >= 4
Requires:	nss-devel >= 3
Requires:	sqlite3-devel >= 3.7.17

%description devel
This package contains the files necessary to develop applications
using Evolution's data server libraries.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki potrzebne do tworzenia aplikacji
korzystających z bibliotek serwera danych Evolution.

%package apidocs
Summary:	Evolution data server API documentation
Summary(pl.UTF-8):	Dokumentacja API serwera danych Evolution
Group:		Documentation
Requires:	gtk-doc-common
BuildArch:	noarch

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
BuildArch:	noarch

%description -n vala-evolution-data-server
Evolution data server API for Vala language.

%description -n vala-evolution-data-server -l pl.UTF-8
API serwera danych Evolution dla języka Vala.

%package gtk3-libs
Summary:	Evolution data server GTK+ 3 UI library
Summary(pl.UTF-8):	Biblioteka interfejsu użytkownika GTK+ 3 serwera danych Evolution
Group:		X11/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	gtk+3 >= 3.20
Requires:	gtk-webkit4.1 >= 2.34.0

%description gtk3-libs
Evolution data server GTK+ 3 UI library.

%description gtk3-libs -l pl.UTF-8
Biblioteka interfejsu użytkownika GTK+ 3 serwera danych Evolution.

%package gtk3-devel
Summary:	Header files for Evolution data server GTK+ 3 UI library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki interfejsu użytkownika GTK+ 3 serwera danych Evolution
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-gtk3-libs = %{version}-%{release}
Requires:	gtk+3-devel >= 3.20

%description gtk3-devel
Header files for Evolution data server GTK+ 3 UI library.

%description gtk3-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki interfejsu użytkownika GTK+ 3 serwera
danych Evolution.

%package -n vala-evolution-data-server-gtk3
Summary:	Vala API for Evolution data server GTK+ 3 UI library
Summary(pl.UTF-8):	API języka Vala do biblioteki interfejsu użytkownika GTK+ 3 serwera danych Evolution
Group:		X11/Development/Libraries
Requires:	%{name}-gtk3-devel = %{version}-%{release}
Requires:	vala-evolution-data-server = %{version}-%{release}
BuildArch:	noarch

%description -n vala-evolution-data-server-gtk3
Vala API for Evolution data server GTK+ 3 UI library.

%description -n vala-evolution-data-server-gtk3 -l pl.UTF-8
API języka Vala do biblioteki interfejsu użytkownika GTK+ 3 serwera
danych Evolution.

%package gtk4-libs
Summary:	Evolution data server GTK 4 UI library
Summary(pl.UTF-8):	Biblioteka interfejsu użytkownika GTK 4 serwera danych Evolution
Group:		X11/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	gtk4 >= 4.4
Requires:	gtk-webkit6 >= 2.40.0

%description gtk4-libs
Evolution data server GTK 4 UI library.

%description gtk4-libs -l pl.UTF-8
Biblioteka interfejsu użytkownika GTK 4 serwera danych Evolution.

%package gtk4-devel
Summary:	Header files for Evolution data server GTK 4 UI library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki interfejsu użytkownika GTK 4 serwera danych Evolution
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-gtk4-libs = %{version}-%{release}
Requires:	gtk4-devel >= 4.4

%description gtk4-devel
Header files for Evolution data server GTK 4 UI library.

%description gtk4-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki interfejsu użytkownika GTK 4 serwera
danych Evolution.

%package -n vala-evolution-data-server-gtk4
Summary:	Vala API for Evolution data server GTK 4 UI library
Summary(pl.UTF-8):	API języka Vala do biblioteki interfejsu użytkownika GTK 4 serwera danych Evolution
Group:		X11/Development/Libraries
Requires:	%{name}-gtk4-devel = %{version}-%{release}
Requires:	vala-evolution-data-server = %{version}-%{release}
BuildArch:	noarch

%description -n vala-evolution-data-server-gtk4
Vala API for Evolution data server GTK 4 UI library.

%description -n vala-evolution-data-server-gtk4 -l pl.UTF-8
API języka Vala do biblioteki interfejsu użytkownika GTK 4 serwera
danych Evolution.

%prep
%setup -q
%patch -P0 -p1

%build
%cmake -B build \
	-DLIBEXEC_INSTALL_DIR=%{_libexecdir} \
	%{?with_kerberos5:-DWITH_KRB5=%{_prefix} -DWITH_KRB5_LIBS=%{_libdir}} \
	%{cmake_on_off kerberos5 WITH_KRB5} \
	%{cmake_on_off ldap WITH_OPENLDAP} \
	%{cmake_on_off apidocs ENABLE_GTK_DOC} \
	%{cmake_on_off vala ENABLE_VALA_BINDINGS} \
	%{cmake_on_off goa ENABLE_GOA} \
	-DENABLE_SCHEMAS_COMPILE=OFF \
	-DENABLE_INTROSPECTION=ON \
	%{?with_phonenumber:-DWITH_PHONENUMBER=ON}

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{schemadir}

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p src/addressbook/backends/ldap/evolutionperson.schema $RPM_BUILD_ROOT%{schemadir}

%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang %{name}

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

%post	gtk3-libs -p /sbin/ldconfig
%postun	gtk3-libs -p /sbin/ldconfig

%post	gtk4-libs -p /sbin/ldconfig
%postun	gtk4-libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS* README
%attr(755,root,root) %{_libexecdir}/camel-gpg-photo-saver
%attr(755,root,root) %{_libexecdir}/camel-index-control-%{apiver}
%attr(755,root,root) %{_libexecdir}/camel-lock-helper-%{apiver}
%attr(755,root,root) %{_libexecdir}/evolution-addressbook-factory-subprocess
%attr(755,root,root) %{_libexecdir}/evolution-addressbook-factory
%attr(755,root,root) %{_libexecdir}/evolution-calendar-factory-subprocess
%attr(755,root,root) %{_libexecdir}/evolution-calendar-factory
%attr(755,root,root) %{_libexecdir}/evolution-scan-gconf-tree-xml
%attr(755,root,root) %{_libexecdir}/evolution-source-registry
%attr(755,root,root) %{_libexecdir}/evolution-user-prompter
%if "%{_libexecdir}" != "%{_libdir}"
%dir %{_libexecdir}/%{name}
%endif
%attr(755,root,root) %{_libexecdir}/%{name}/addressbook-export
%attr(755,root,root) %{_libexecdir}/%{name}/csv2vcard
%attr(755,root,root) %{_libexecdir}/%{name}/evolution-alarm-notify
%attr(755,root,root) %{_libexecdir}/%{name}/evolution-oauth2-handler
%attr(755,root,root) %{_libexecdir}/%{name}/list-sources
%dir %{_libdir}/%{name}/addressbook-backends
%attr(755,root,root) %{_libdir}/%{name}/addressbook-backends/libebookbackendfile.so
%attr(755,root,root) %{_libdir}/%{name}/addressbook-backends/libebookbackendcarddav.so
%dir %{_libdir}/%{name}/calendar-backends
%attr(755,root,root) %{_libdir}/%{name}/calendar-backends/libecalbackendcaldav.so
%attr(755,root,root) %{_libdir}/%{name}/calendar-backends/libecalbackendcontacts.so
%attr(755,root,root) %{_libdir}/%{name}/calendar-backends/libecalbackendfile.so
%attr(755,root,root) %{_libdir}/%{name}/calendar-backends/libecalbackendgtasks.so
%attr(755,root,root) %{_libdir}/%{name}/calendar-backends/libecalbackendhttp.so
%attr(755,root,root) %{_libdir}/%{name}/calendar-backends/libecalbackendweather.so
%attr(755,root,root) %{_libdir}/%{name}/calendar-backends/libecalbackendwebdavnotes.so
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
%if %{with goa}
%attr(755,root,root) %{_libdir}/%{name}/credential-modules/module-credentials-goa.so
%endif
%dir %{_libdir}/evolution-data-server/registry-modules
%attr(755,root,root) %{_libdir}/evolution-data-server/registry-modules/module-cache-reaper.so
%if %{with goa}
%attr(755,root,root) %{_libdir}/evolution-data-server/registry-modules/module-gnome-online-accounts.so
%endif
%attr(755,root,root) %{_libdir}/evolution-data-server/registry-modules/module-google-backend.so
%attr(755,root,root) %{_libdir}/evolution-data-server/registry-modules/module-oauth2-services.so
%attr(755,root,root) %{_libdir}/evolution-data-server/registry-modules/module-outlook-backend.so
%attr(755,root,root) %{_libdir}/evolution-data-server/registry-modules/module-secret-monitor.so
%attr(755,root,root) %{_libdir}/evolution-data-server/registry-modules/module-trust-prompt.so
%attr(755,root,root) %{_libdir}/evolution-data-server/registry-modules/module-webdav-backend.so
%attr(755,root,root) %{_libdir}/evolution-data-server/registry-modules/module-yahoo-backend.so
%dir %{_datadir}/evolution-data-server
%{_datadir}/evolution-data-server/icons

%{systemduserunitdir}/evolution-addressbook-factory.service
%{systemduserunitdir}/evolution-calendar-factory.service
%{systemduserunitdir}/evolution-source-registry.service
%{systemduserunitdir}/evolution-user-prompter.service

%{_iconsdir}/hicolor/scalable/apps/org.gnome.Evolution-alarm-notify.svg
%{_pixmapsdir}/%{name}

%{_datadir}/dbus-1/services/org.gnome.evolution.dataserver.AddressBook10.service
%{_datadir}/dbus-1/services/org.gnome.evolution.dataserver.Calendar8.service
%{_datadir}/dbus-1/services/org.gnome.evolution.dataserver.Sources5.service
%{_datadir}/dbus-1/services/org.gnome.evolution.dataserver.UserPrompter0.service

%{_datadir}/GConf/gsettings/evolution-data-server.convert
%{_datadir}/glib-2.0/schemas/org.gnome.evolution.eds-shell.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.evolution.shell.network-config.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.Evolution.DefaultSources.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.evolution-data-server.addressbook.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.evolution-data-server.calendar.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.evolution-data-server.gschema.xml

%{_sysconfdir}/xdg/autostart/org.gnome.Evolution-alarm-notify.desktop
%{_desktopdir}/org.gnome.Evolution-alarm-notify.desktop
%{_desktopdir}/org.gnome.evolution-data-server.OAuth2-handler.desktop

%if %{with ldap}
%files ldap
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/addressbook-backends/libebookbackendldap.so
%{_datadir}/%{name}/evolutionperson.schema
%endif

%files -n openldap-schema-evolutionperson
%defattr(644,root,root,755)
%{schemadir}/evolutionperson.schema

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcamel-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcamel-%{apiver}.so.64
%attr(755,root,root) %{_libdir}/libebackend-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libebackend-%{apiver}.so.11
%attr(755,root,root) %{_libdir}/libebook-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libebook-%{apiver}.so.21
%attr(755,root,root) %{_libdir}/libebook-contacts-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libebook-contacts-%{apiver}.so.4
%attr(755,root,root) %{_libdir}/libecal-%{cal_apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libecal-%{cal_apiver}.so.3
%attr(755,root,root) %{_libdir}/libedata-book-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libedata-book-%{apiver}.so.27
%attr(755,root,root) %{_libdir}/libedata-cal-%{cal_apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libedata-cal-%{cal_apiver}.so.2
%attr(755,root,root) %{_libdir}/libedataserver-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libedataserver-%{apiver}.so.27
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/libedbus-private.so
%{_libdir}/girepository-1.0/Camel-1.2.typelib
%{_libdir}/girepository-1.0/EBackend-%{apiver}.typelib
%{_libdir}/girepository-1.0/EBook-%{apiver}.typelib
%{_libdir}/girepository-1.0/EBookContacts-%{apiver}.typelib
%{_libdir}/girepository-1.0/ECal-%{cal_apiver}.typelib
%{_libdir}/girepository-1.0/EDataBook-%{apiver}.typelib
%{_libdir}/girepository-1.0/EDataCal-%{cal_apiver}.typelib
%{_libdir}/girepository-1.0/EDataServer-%{apiver}.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcamel-%{apiver}.so
%attr(755,root,root) %{_libdir}/libebackend-%{apiver}.so
%attr(755,root,root) %{_libdir}/libebook-%{apiver}.so
%attr(755,root,root) %{_libdir}/libebook-contacts-%{apiver}.so
%attr(755,root,root) %{_libdir}/libecal-%{cal_apiver}.so
%attr(755,root,root) %{_libdir}/libedata-book-%{apiver}.so
%attr(755,root,root) %{_libdir}/libedata-cal-%{cal_apiver}.so
%attr(755,root,root) %{_libdir}/libedataserver-%{apiver}.so
%dir %{_includedir}/evolution-data-server
%{_includedir}/evolution-data-server/camel
%{_includedir}/evolution-data-server/libebackend
%{_includedir}/evolution-data-server/libebook
%{_includedir}/evolution-data-server/libebook-contacts
%{_includedir}/evolution-data-server/libecal
%{_includedir}/evolution-data-server/libedata-book
%{_includedir}/evolution-data-server/libedata-cal
%{_includedir}/evolution-data-server/libedataserver
%{_pkgconfigdir}/camel-%{apiver}.pc
%{_pkgconfigdir}/evolution-data-server-%{apiver}.pc
%{_pkgconfigdir}/libebackend-%{apiver}.pc
%{_pkgconfigdir}/libebook-%{apiver}.pc
%{_pkgconfigdir}/libebook-contacts-%{apiver}.pc
%{_pkgconfigdir}/libecal-%{cal_apiver}.pc
%{_pkgconfigdir}/libedata-book-%{apiver}.pc
%{_pkgconfigdir}/libedata-cal-%{cal_apiver}.pc
%{_pkgconfigdir}/libedataserver-%{apiver}.pc
%{_datadir}/gir-1.0/Camel-1.2.gir
%{_datadir}/gir-1.0/EBackend-%{apiver}.gir
%{_datadir}/gir-1.0/EBook-%{apiver}.gir
%{_datadir}/gir-1.0/EBookContacts-%{apiver}.gir
%{_datadir}/gir-1.0/ECal-%{cal_apiver}.gir
%{_datadir}/gir-1.0/EDataBook-%{apiver}.gir
%{_datadir}/gir-1.0/EDataCal-%{cal_apiver}.gir
%{_datadir}/gir-1.0/EDataServer-%{apiver}.gir

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/camel
%{_gtkdocdir}/evolution-data-server
%endif

%if %{with vala}
%files -n vala-evolution-data-server
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/camel-1.2.deps
%{_datadir}/vala/vapi/camel-1.2.vapi
%{_datadir}/vala/vapi/libebackend-%{apiver}.deps
%{_datadir}/vala/vapi/libebackend-%{apiver}.vapi
%{_datadir}/vala/vapi/libebook-%{apiver}.deps
%{_datadir}/vala/vapi/libebook-%{apiver}.vapi
%{_datadir}/vala/vapi/libebook-contacts-%{apiver}.deps
%{_datadir}/vala/vapi/libebook-contacts-%{apiver}.vapi
%{_datadir}/vala/vapi/libecal-%{cal_apiver}.deps
%{_datadir}/vala/vapi/libecal-%{cal_apiver}.vapi
%{_datadir}/vala/vapi/libedata-book-%{apiver}.deps
%{_datadir}/vala/vapi/libedata-book-%{apiver}.vapi
%{_datadir}/vala/vapi/libedata-cal-%{cal_apiver}.deps
%{_datadir}/vala/vapi/libedata-cal-%{cal_apiver}.vapi
%{_datadir}/vala/vapi/libedataserver-%{apiver}.deps
%{_datadir}/vala/vapi/libedataserver-%{apiver}.vapi
%endif

%files gtk3-libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libedataserverui-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libedataserverui-%{apiver}.so.4
%{_libdir}/girepository-1.0/EDataServerUI-%{apiver}.typelib

%files gtk3-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libedataserverui-%{apiver}.so
%{_includedir}/evolution-data-server/libedataserverui
%{_datadir}/gir-1.0/EDataServerUI-%{apiver}.gir
%{_pkgconfigdir}/libedataserverui-%{apiver}.pc

%if %{with vala}
%files -n vala-evolution-data-server-gtk3
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/libedataserverui-%{apiver}.deps
%{_datadir}/vala/vapi/libedataserverui-%{apiver}.vapi
%endif

%files gtk4-libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libedataserverui4-%{ui4_apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libedataserverui4-%{ui4_apiver}.so.0
%{_libdir}/girepository-1.0/EDataServerUI4-%{ui4_apiver}.typelib

%files gtk4-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libedataserverui4-%{ui4_apiver}.so
%{_datadir}/gir-1.0/EDataServerUI4-%{ui4_apiver}.gir
%{_includedir}/evolution-data-server/libedataserverui4
%{_pkgconfigdir}/libedataserverui4-%{ui4_apiver}.pc

%if %{with vala}
%files -n vala-evolution-data-server-gtk4
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/libedataserverui4-%{ui4_apiver}.deps
%{_datadir}/vala/vapi/libedataserverui4-%{ui4_apiver}.vapi
%endif
