%define url_ver	%(echo %{version}|cut -d. -f1,2)
%define _disable_rebuild_configure 1

%define api		0
%define gi_major	0.1
%define lib_major	0

%define lib_name	%mklibname %{name} %{api} %{lib_major}
%define gi_name		%mklibname %{name}-gir %{gi_major}
%define develname	%mklibname -d %{name}

Name:		gnome-autoar
Version:	0.4.0
Release:	1
Summary:	Archive library

Group:		System/Libraries
License:	LGPLv2+
URL:		https://git.gnome.org/browse/gnome-autoar
Source0:	https://download.gnome.org/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz

BuildRequires:  meson
BuildRequires:  pkgconfig(gtk-doc)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libarchive)
BuildRequires:  pkgconfig(vapigen)

%description
%{name} is a GObject based library for handling archives.

%package -n %{lib_name}
Summary:	Archive library
Obsoletes:	%{name} < 0.2.0
Obsoletes:	%{_lib}gnome-autoar0 < 0.2.0

%description -n %{lib_name}
%{name} is a GObject based library for handling archives.

%package -n %{gi_name}
Summary:	GObject Introspection interface library for %{name}
Group:		System/Libraries
Requires:	%{lib_name} = %{version}-%{release}

%description -n %{gi_name}
GObject Introspection interface library for %{name}.

%package        -n %{develname}
Summary:	Development files for %{name}
Requires:	%{lib_name} = %{version}-%{release}
Requires:	%{gi_name} = %{version}-%{release}

%description    -n %{develname}
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1

%build
%meson  \
        -Dgtk=true \
        -Dintrospection=enabled \
        -Dvapi=true \
        -Dgtk_doc=true
%meson_build

%install
%meson_install

#we don't want these
find %{buildroot} -name '*.la' -delete

%files -n %{lib_name}
%doc COPYING
%{_libdir}/libgnome-autoar-%{api}.so.%{lib_major}*
%{_libdir}/libgnome-autoar-gtk-%{api}.so.%{lib_major}*

%files -n %{gi_name}
%{_libdir}/girepository-1.0/GnomeAutoar-%{gi_major}.typelib
%{_libdir}/girepository-1.0/GnomeAutoarGtk-%{gi_major}.typelib

%files -n %{develname}
%doc NEWS
%doc %{_datadir}/gtk-doc/html/gnome-autoar/
%{_includedir}/gnome-autoar-%{api}/
%{_libdir}/pkgconfig/gnome-autoar-%{api}.pc
%{_libdir}/pkgconfig/gnome-autoar-gtk-%{api}.pc
%{_libdir}/libgnome-autoar-%{api}.so
%{_libdir}/libgnome-autoar-gtk-%{api}.so
%{_datadir}/gir-1.0/GnomeAutoar-%{gi_major}.gir
%{_datadir}/gir-1.0/GnomeAutoarGtk-%{gi_major}.gir
%{_datadir}/vala/vapi/gnome-autoar-*
