#
# todo:
# - system libical
#
# Conditional build:
%bcond_without	kerberos5	# build without kerberos5 support
%bcond_without	ldap		# build without ldap support
#
%define		basever		1.10
%define		apiver		1.2
Summary:	Evolution data server
Summary(pl.UTF-8):	Serwer danych Evolution
Name:		evolution-data-server
Version:	1.10.3.1
Release:	1
License:	GPL
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/evolution-data-server/1.10/%{name}-%{version}.tar.bz2
# Source0-md5:	c6f804ac25f7c75dc9502b739bf99301
Patch0:		%{name}-as_needed-fix.patch
URL:		http://www.ximian.com/products/ximian_evolution/
BuildRequires:	ORBit2-devel >= 1:2.14.7
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	db-devel
BuildRequires:	gnome-common >= 2.18.0
BuildRequires:	gnome-keyring-devel >= 0.8.1
BuildRequires:	gtk-doc >= 1.8
%{?with_kerberos5:BuildRequires:	krb5-devel}
BuildRequires:	intltool >= 0.35.5
BuildRequires:	libglade2-devel >= 1:2.6.0
BuildRequires:	libgnomeui-devel >= 2.18.1
BuildRequires:	libsoup-devel >= 2.2.100
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
Group:		Libraries
Requires:	libgnomeui >= 2.18.1
Requires:	libsoup >= 2.2.100

%description libs
This package contains Evolution Data Server library.

%description libs -l pl.UTF-8
Ten pakiet zawiera bibliotekę Evolution Data Server.

%package devel
Summary:	Evolution data server development files
Summary(pl.UTF-8):	Pliki programistyczne serwera danych evolution
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
%{?with_kerberos5:Requires:	krb5-devel}
# for all but libegroupwise
Requires:	GConf2-devel >= 2.18.0.1
Requires:	ORBit2-devel >= 1:2.14.7
Requires:	glib2-devel >= 1:2.12.11
Requires:	libgnomeui-devel >= 2.18.1
Requires:	libxml2-devel >= 1:2.6.27
# for libegroupwise
Requires:	libsoup-devel >= 2.2.100

%description devel
This package contains the files necessary to develop applications
using Evolution's data server libraries.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki potrzebne do tworzenia aplikacji
korzystających z bibliotek serwera danych Evolution.

%package static
Summary:	Evolution data server static libraries
Summary(pl.UTF-8):	Statyczne biblioteki serwera danych Evolution
Group:		Development/Libraries
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
%dir %{_libdir}/%{name}-%{apiver}
%dir %{_libdir}/%{name}-%{apiver}/camel-providers
%attr(755,root,root) %{_libdir}/evolution-data-server-%{basever}
%attr(755,root,root) %{_libdir}/%{name}-%{apiver}/camel-providers/*.so
%{_libdir}/%{name}-%{apiver}/camel-providers/*.urls
%dir %{_libdir}/%{name}-%{apiver}/extensions
%attr(755,root,root) %{_libdir}/%{name}-%{apiver}/extensions/*.so
%{_libdir}/bonobo/servers/*

%if %{with ldap}
%{_datadir}/%{name}-%{basever}/*.schema
%endif

%dir %{_datadir}/%{name}-%{basever}
%{_datadir}/%{name}-%{basever}/glade
%{_datadir}/%{name}-%{basever}/weather
%{_datadir}/%{name}-%{basever}/zoneinfo
%{_pixmapsdir}/%{name}

%files -n openldap-schema-evolutionperson
%defattr(644,root,root,755)
%{schemadir}/*.schema

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so.*.*
%{_datadir}/idl/%{name}-%{apiver}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/*
%{_pkgconfigdir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/*
