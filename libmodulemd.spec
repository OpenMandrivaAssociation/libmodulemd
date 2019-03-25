%define major 2
%define girapi %{major}.0
%define libname %mklibname modulemd %{major}
%define girname %mklibname modulemd-gir %{girapi}
%define devname %mklibname modulemd -d

# Legacy modulemd API needed for DNF
%define oldversion 1.8.2
%define oldmajor 1
%define oldgirapi %{oldmajor}.0
%define oldlibname %mklibname modulemd %{oldmajor}
%define oldgirname %mklibname modulemd-gir %{oldgirapi}
%define olddevname %mklibname modulemd %{oldmajor} -d

%define newversion 2.1.0

%bcond_without gir
%bcond_with gtk-doc

Summary:	Library for manipulating module metadata files
Name:		libmodulemd
Version:	%{newversion}
Release:	1
Group:		System/Libraries
License:	LGPLv2+
URL:		https://github.com/fedora-modularity/%{name}
Source0:	https://github.com/fedora-modularity/libmodulemd/archive/modulemd-%{newversion}.tar.xz
Patch0:		disable-gtk-doc.patch
BuildRequires:	meson
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	python3egg(autopep8)
BuildRequires:	python3dist(pygobject)
BuildRequires:	pkgconfig(yaml-0.1)
%if %{with gtk-doc}
BuildRequires:	gtk-doc
%endif
#BuildRequires:	valgrind

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

%package -n %{oldlibname}
Summary:        Main library for %{name} 1.x
Version:        %{oldversion}
Group:          System/Libraries

%description -n %{oldlibname}
This package provides the main library for applications
that use %{name} 1.x.

%package -n %{oldgirname}
Summary:        GObject Introspection interface description for %{name} 1.x
Version:        %{oldversion}
Group:          System/Libraries
Requires:       %{oldlibname}%{?_isa} = %{oldversion}-%{release}

%description -n %{oldgirname}
This package provides the GObject Introspection typelib interface
for applications to use %{name} 1.x.

%package -n %{olddevname}
Summary:        Development files for %{name} 1.x
Version:        %{oldversion}
Group:          Development/C
Conflicts:      %{devname}
Provides:       %{name}%{oldmajor}-devel = %{oldversion}-%{release}
Provides:       %{name}%{oldmajor}-devel%{?_isa} = %{oldversion}-%{release}
Provides:       modulemd%{oldmajor}-devel = %{oldversion}-%{release}
Provides:       modulemd%{oldmajor}-devel%{?_isa} = %{oldversion}-%{release}
Requires:       %{oldlibname}%{?_isa} = %{oldversion}-%{release}
Requires:       %{oldgirname}%{?_isa} = %{oldversion}-%{release}
RemovePathPostfixes: .compat

%description -n %{olddevname}
This package provides files for developing applications to use %{name} 1.x.

%prep
%autosetup -p1 -n modulemd-%{newversion}

%build
%meson -Ddeveloper_build=false \
	-Dbuild_api_v1=true \
%if !%{with gir}
	-Dskip_introspection=true \
%endif
	-Dbuild_api_v2=true \

%ninja_build -C build

%install
%ninja_install -C build
ln -s %{_libdir}/%{name}.so.%{oldversion} %{buildroot}%{_libdir}/%{name}.so.compat

%files
%{_bindir}/modulemd-validator
%{_bindir}/modulemd-validator-v1

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
%if %{with gtk-doc}
%doc %{_datadir}/gtk-doc/html/modulemd-%{girapi}
%endif

%files -n python-%{name}
%{py_platsitedir}/gi/overrides/Modulemd.py
%{py_platsitedir}/gi/overrides/__pycache__/Modulemd.*

%files -n %{oldlibname}
%{_libdir}/%{name}.so.%{oldmajor}*

%files -n %{oldgirname}
%{_libdir}/girepository-1.0/Modulemd-%{oldgirapi}.typelib

%files -n %{olddevname}
%{_libdir}/%{name}.so.compat
%{_libdir}/pkgconfig/modulemd.pc
%{_includedir}/modulemd/
%{_datadir}/gir-1.0/Modulemd-%{oldgirapi}.gir
%if %{with gtk-doc}
%doc %{_datadir}/gtk-doc/html/modulemd-%{oldgirapi}/
%endif
