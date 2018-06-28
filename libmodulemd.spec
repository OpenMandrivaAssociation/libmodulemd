%define major 1
%define girapi %{major}.0
%define libname %mklibname modulemd %{major}
%define girname %mklibname modulemd-gir %{girapi}
%define devname %mklibname modulemd -d

Summary:	Library for manipulating module metadata files
Name:		libmodulemd
Version:	1.5.2
Release:	1
Group:		System/Libraries
License:	LGPLv2+
URL:		https://github.com/fedora-modularity/%{name}
Source0:	https://github.com/fedora-modularity/libmodulemd/archive/libmodulemd-%{version}.tar.gz

BuildRequires:	meson
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	python3egg(autopep8)
BuildRequires:	pkgconfig(yaml-0.1)

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

%description -n %{devname}
Development files for %{name}.

%prep
%autosetup -p1 -n %{name}-%{name}-%{version}

%build
%meson
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
%{_datadir}/gir-1.0/Modulemd-*.gir
%{_includedir}/modulemd
%{_libdir}/pkgconfig/modulemd.pc
%doc %{_datadir}/gtk-doc/html/modulemd
