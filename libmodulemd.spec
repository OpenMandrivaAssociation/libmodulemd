%define major 2
%define girapi %{major}.0
%define oldlibname %mklibname modulemd 2
%define libname %mklibname modulemd
%define girname %mklibname modulemd-gir %{girapi}
%define devname %mklibname modulemd -d
%define girdev %mklibname modulemd-gir -d

%bcond_without gir
%bcond_without python
%bcond_with gtk-doc

Summary:	Library for manipulating module metadata files
Name:		libmodulemd
Version:	2.15.2
Release:	1
Group:		System/Libraries
License:	LGPLv2+
URL:		https://github.com/fedora-modularity/libmodulemd
Source0:	https://github.com/fedora-modularity/libmodulemd/releases/download/modulemd-%{version}/modulemd-%{version}.tar.xz
BuildRequires:	meson
BuildRequires:	cmake
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	python%{pyver}dist(autopep8)
BuildRequires:	python%{pyver}dist(pygobject)
BuildRequires:	pkgconfig(yaml-0.1)
BuildRequires:	pkgconfig(rpm)
BuildRequires:	magic-devel
BuildRequires:	/bin/sh
BuildRequires:	sed
BuildRequires:	coreutils
BuildRequires:	help2man
%if %{with gtk-doc}
BuildRequires:	gtk-doc
%endif
#BuildRequires:	valgrind

%description
Library for manipulating module metadata files

%package -n %{libname}
Summary:	Library for manipulating module metadata files
Group:		System/Libraries
%rename %{oldlibname}

%description -n %{libname}
Library for manipulating module metadata files

%package -n %{girname}
Summary:	GObject Introspection interface description for libmodulemd
Group:		System/Libraries
Requires:	%{libname}%{?_isa} = %{EVRD}

%description -n %{girname}
GObject Introspection interface description for libmodulemd.

%package -n %{girdev}
Summary:	Development files for the GObject Introspection interface description for libmodulemd
Group:		System/Libraries
Requires:	%{girname}%{?_isa} = %{EVRD}
Requires:	%{devname}%{?_isa} = %{EVRD}

%description -n %{girdev}
Development files for the GObject Introspection interface description for libmodulemd

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Provides:	%{name}-devel%{?_isa} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname}%{?_isa} = %{version}-%{release}

%package -n python-%{name}
Summary:	Python bindings for %{name}
Group:		Development/Python
Requires:	%{girname}%{?_isa} = %{version}-%{release}
Requires:	python3dist(pygobject)

%description -n python-%{name}
This package provides the Python 3 bindings for %{name}.

%description -n %{devname}
Development files for %{name}.

%prep
%autosetup -p1 -n modulemd-%{version}

# https://github.com/fedora-modularity/libmodulemd/issues/387
sed -i -e 's,/usr/bin/sh,/bin/sh,g' modulemd/clang_simple_version.sh

%build
%meson \
%if !%{with gir}
	-Dskip_introspection=true \
%endif
%if %{without gtk-doc}
	-Dwith_docs=false \
%endif
%if %{without python}
	-Dwith_py3=false \
%endif
	-Dgobject_overrides_dir_py3=

%ninja_build -C build

%install
%ninja_install -C build

%files
%{_bindir}/modulemd-validator
%doc %{_mandir}/man1/modulemd-validator.1.*

%files -n %{libname}
%{_libdir}/%{name}.so.%{major}*

%if %{with gir}
%files -n %{girname}
%{_libdir}/girepository-1.0/Modulemd-%{girapi}.typelib

%files -n %{girdev}
%{_datadir}/gir-1.0/Modulemd-%{girapi}.gir
%if %{with gtk-doc}
%doc %{_datadir}/gtk-doc/html/modulemd-%{girapi}
%endif
%endif

%files -n %{devname}
%license COPYING
%{_libdir}/%{name}.so
%{_includedir}/modulemd-%{major}.0
%{_libdir}/pkgconfig/modulemd-%{major}*.pc

%if %{with python}
%files -n python-%{name}
%{py_platsitedir}/gi/overrides/Modulemd.py
%endif
