
#
# todo:
# - system libical
#

%define		mver		1.0

Summary:	Evolution data server
Name:		evolution-data-server
Version:	0.0.3
Release:	0.10
License:	GPL
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/%{name}/0.0/%{name}-%{version}.tar.gz
# Source0-md5:	bcacfd623db973a100deb67f0b7d8a38
Patch0:		%{name}-system_db.patch
URL:		http://www.ximian.com/products/ximian_evolution/
BuildRequires:	libsoup-devel >= 2.1.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Requires(post,postun):	/sbin/ldconfig
Requires(post,postun):	/usr/bin/scrollkeeper-update
Requires(post):		GConf2

%description
Evolution data server.

%package devel
Summary:	Evolution data server development files
Group:		Development/Libraries
Requires:	%{name} >= %{version}

%description devel
This package contains the files necessary to develop applications
using Evolution's data server libraries.

%package static
Summary:	Evolution data server static libraries
Group:		Development/Libraries
Requires:	%{name}-devel >= %{version}

%description static
Evolution data server static libraries.

%prep
%setup -q 
%patch0 -p1
rm -rf libdb/

%build
glib-gettextize --copy --force
intltoolize --copy --force
%{__libtoolize}
%{__aclocal} -I %{_aclocaldir}/gnome2-macros
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--enable-gtk-doc \
	--enable-static \
	--with-openldap=yes

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
%attr(755,root,root) %{_libdir}/%{name}-1.0
%attr(755,root,root) %{_libdir}/*.so.*.*
%{_libdir}/bonobo/servers/*
%{_datadir}/idl/*
%dir %{_datadir}/%{name}-%{mver}
%{_datadir}/%{name}-%{mver}/zoneinfo
%{_datadir}/%{name}-%{mver}/*.schema

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
