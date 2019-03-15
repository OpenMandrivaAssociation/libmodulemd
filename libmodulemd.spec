%define major 2
%define girapi %{major}.0
%define libname %mklibname modulemd %{major}
%define girname %mklibname modulemd-gir %{girapi}
%define devname %mklibname modulemd -d

Summary:	Library for manipulating module metadata files
Name:		libmodulemd
Version:	2.1.0
Release:	1
Group:		System/Libraries
License:	LGPLv2+
URL:		https://github.com/fedora-modularity/%{name}
Source0:	https://github.com/fedora-modularity/libmodulemd/archive/modulemd-%{version}.tar.xz
BuildRequires:	meson
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	python3egg(autopep8)
BuildRequires:	python3dist(pygobject)
BuildRequires:	pkgconfig(yaml-0.1)
BuildRequires:	gtk-doc
BuildRequires:	valgrind

%description
Library for manipulating module metadata files

%package -n %{libname}
Summary:	Library for manipulating module metadata files
Group:		System/Libraries

%description -n %{libname}
Library for manipulating module metadata files

%package -n %{girname}
Summary:	GObject Introspection interface description for libmodulemd
Group:		System/Libraries
Requires:	%{libname}%{?_isa} = %{version}-%{release}

%description -n %{girname}
GObject Introspection interface description for libmodulemd.

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Provides:	%{name}-devel%{?_isa} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{girname}%{?_isa} = %{version}-%{release}
Requires:	%{libname}%{?_isa} = %{version}-%{release}

%package -n python-%{name}
Summary:        Python bindings for %{name}
Group:          Development/Python
Requires:       %{girname}%{?_isa} = %{version}-%{release}
Requires:       python3dist(pygobject)

%description -n python-%{name}
This package provides the Python 3 bindings for %{name}.

%description -n %{devname}
Development files for %{name}.

%prep
%autosetup -p1 -n modulemd-%{version}

%build
%meson -Ddeveloper_build=false
%ninja_build -C build

%install
%ninja_install -C build

%files
%{_bindir}/modulemd-validator

%files -n %{libname}
%{_libdir}/%{name}.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/Modulemd-%{girapi}.typelib

%files -n %{devname}
%license COPYING
%{_libdir}/%{name}.so
%{_datadir}/gir-1.0/Modulemd-%{girapi}.gir
%{_includedir}/modulemd-%{major}.0
%{_libdir}/pkgconfig/modulemd-%{major}*.pc
%doc %{_datadir}/gtk-doc/html/modulemd-%{girapi}

%files -n python-%{name}
%{py_platsitedir}/gi/overrides/Modulemd.py
%{py_platsitedir}/gi/overrides/__pycache__/Modulemd.*
