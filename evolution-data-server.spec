#
# todo:
# - system libical
#
# Conditional build:
%bcond_without	kerberos5	# build without kerberos5 support
%bcond_without	ldap		# build without ldap support
#
%define		basever		2.22
%define		apiver		1.2
Summary:	Evolution data server
Summary(pl.UTF-8):	Serwer danych Evolution
Name:		evolution-data-server
Version:	2.22.1.1
Release:	2
License:	LGPL v2+
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/evolution-data-server/2.22/%{name}-%{version}.tar.bz2
# Source0-md5:	53517ab651ba2a6fe57e00ef438c2ccb
Patch0:		%{name}-ntlm-ldap.patch
Patch1:		%{name}-passwords.patch
URL:		http://www.gnome.org/projects/evolution/
BuildRequires:	GConf2-devel >= 2.22.0
BuildRequires:	ORBit2-devel >= 1:2.14.8
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	cyrus-sasl-devel
BuildRequires:	db-devel
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.16.1
BuildRequires:	gnome-common >= 2.20.0
BuildRequires:	gnome-keyring-devel >= 2.22.0
BuildRequires:	gnome-vfs2-devel >= 2.22.0
BuildRequires:	gtk+2-devel >= 2:2.12.8
BuildRequires:	gtk-doc >= 1.9
BuildRequires:	intltool >= 0.37.0
%{?with_kerberos5:BuildRequires:	krb5-devel}
BuildRequires:	libglade2-devel >= 1:2.6.2
BuildRequires:	libgnomeui-devel >= 2.22.01
BuildRequires:	libsoup-devel >= 2.4.0
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
Requires:	libgnomeui >= 2.22.01
Requires:	libsoup >= 2.4.0

%description libs
This package contains Evolution Data Server library.

%description libs -l pl.UTF-8
Ten pakiet zawiera bibliotekę Evolution Data Server.

%package devel
Summary:	Evolution data server development files
Summary(pl.UTF-8):	Pliki programistyczne serwera danych evolution
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
%{?with_kerberos5:Requires:	krb5-devel}
# for all but libegroupwise
Requires:	GConf2-devel >= 2.22.0
Requires:	ORBit2-devel >= 1:2.14.8
Requires:	glib2-devel >= 1:2.16.1
Requires:	gtk+2-devel >= 2:2.12.8
Requires:	libglade2-devel >= 1:2.6.2
Requires:	libgnomeui-devel >= 2.22.0
Requires:	libxml2-devel >= 1:2.6.31
# for libegroupwise
Requires:	libsoup-devel >= 2.4.0

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
%patch1 -p0

sed -i -e 's#sr@Latn#sr@latin#' po/LINGUAS
mv po/sr@{Latn,latin}.po

%build
%{__gtkdocize}
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

# Set LIBS so that configure will be able to link with static LDAP libraries,
# which depend on Cyrus SASL and OpenSSL.
if pkg-config openssl ; then
	LIBS="-lsasl2 `pkg-config --libs openssl`"
else
	LIBS="-lsasl2 -lssl -lcrypto"
fi
export LIBS

%configure \
	%{?with_kerberos5:--with-krb5=%{_prefix}} \
	%{!?with_kerberos5:--with-krb5=no} \
	%{?with_ldap:--with-openldap=%{_libdir}/evolution-openldap} \
	%{?with_ldap:--with-static-ldap=yes} \
	%{!?with_ldap:--with-openldap=no} \
	--enable-gnome-keyring=yes \
	--enable-gtk-doc \
	--enable-static \
	--with-nspr-includes=%{_includedir}/nspr \
	--with-nspr-libs=%{_libdir} \
	--with-nss-includes=%{_includedir}/nss \
	--with-nss-libs=%{_libdir} \
	--with-libdb=%{_libdir}

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

install -d $RPM_BUILD_ROOT%{schemadir}
install addressbook/backends/ldap/evolutionperson.schema $RPM_BUILD_ROOT%{schemadir}

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
%{_pixmapsdir}/%{name}

%files -n openldap-schema-evolutionperson
%defattr(644,root,root,755)
%{schemadir}/evolutionperson.schema

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcamel-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcamel-%{apiver}.so.11
%attr(755,root,root) %{_libdir}/libcamel-provider-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcamel-provider-%{apiver}.so.11
%attr(755,root,root) %{_libdir}/libebook-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libebook-%{apiver}.so.9
%attr(755,root,root) %{_libdir}/libecal-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libecal-%{apiver}.so.7
%attr(755,root,root) %{_libdir}/libedata-book-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libedata-book-%{apiver}.so.2
%attr(755,root,root) %{_libdir}/libedata-cal-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libedata-cal-%{apiver}.so.6
%attr(755,root,root) %{_libdir}/libedataserver-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libedataserver-%{apiver}.so.9
%attr(755,root,root) %{_libdir}/libedataserverui-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libedataserverui-%{apiver}.so.8
%attr(755,root,root) %{_libdir}/libegroupwise-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libegroupwise-%{apiver}.so.13
%attr(755,root,root) %{_libdir}/libexchange-storage-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libexchange-storage-%{apiver}.so.3
%attr(755,root,root) %{_libdir}/libgdata-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgdata-%{apiver}.so.1
%attr(755,root,root) %{_libdir}/libgdata-google-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgdata-google-%{apiver}.so.1
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
%attr(755,root,root) %{_libdir}/libgdata-%{apiver}.so
%attr(755,root,root) %{_libdir}/libgdata-google-%{apiver}.so
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
%{_libdir}/libgdata-%{apiver}.la
%{_libdir}/libgdata-google-%{apiver}.la
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
%{_pkgconfigdir}/libgdata-%{apiver}.pc
%{_pkgconfigdir}/libgdata-google-%{apiver}.pc

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
%{_libdir}/libgdata-%{apiver}.a
%{_libdir}/libgdata-google-%{apiver}.a

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/camel
%{_gtkdocdir}/libebook
%{_gtkdocdir}/libecal
%{_gtkdocdir}/libedata-book
%{_gtkdocdir}/libedata-cal
%{_gtkdocdir}/libedataserver
%{_gtkdocdir}/libedataserverui
