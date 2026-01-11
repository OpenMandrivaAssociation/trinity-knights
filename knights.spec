%bcond clang 1

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define pkg_rel 2

%define tde_pkg knights
%define tde_prefix /opt/trinity


%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	0.6
Release:	%{?tde_version}_%{?!preversion:%{pkg_rel}}%{?preversion:0_%{preversion}}%{?dist}
Summary:	A chess interface for the K Desktop Environment [Trinity]
Group:		Amusements/Games
URL:		http://www.trinitydesktop.org/

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}

Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/games/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildSystem:    cmake
BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DCMAKE_INSTALL_PREFIX=%{tde_prefix}
BuildOption:    -DSHARE_INSTALL_PREFIX=%{tde_prefix}/share
BuildOption:    -DWITH_ALL_OPTIONS=ON
BuildOption:    -DBUILD_ALL=ON -DBUILD_DOC=ON
BuildOption:    -DBUILD_TRANSLATIONS=ON
BuildOption:    -DWITH_GCC_VISIBILITY=%{!?with_clang:ON}%{?with_clang:OFF}

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils
BuildRequires:	gettext

BuildRequires:	trinity-tde-cmake >= %{tde_version}

%{!?with_clang:BuildRequires:	gcc-c++}

BuildRequires:	pkgconfig
BuildRequires:	libtool

# ACL support
BuildRequires:  pkgconfig(libacl)

# IDN support
BuildRequires:	pkgconfig(libidn)

# OPENSSL support
BuildRequires:  pkgconfig(openssl)

BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)

# GNUCHESS support
Requires:		gnuchess

%description
Knights aims to be the ultimate chess resource on your computer. 
Written for the K Desktop Environment, it's designed to be both friendly 
to new chess players and functional for Grand Masters.

Here's a quick list of Knights' key features:
* Play against yourself, against computer opponents, 
  or against others over the Internet.
* Customize your board and pieces with over 30 different themes, 
  or make your own!
* Audio cues help alert you to important events.
* Novice players can preview potential moves.
* Save your unfinished matches and play them again later.


%conf -p
unset QTDIR QTINC QTLIB
export PATH="%{tde_prefix}/bin:${PATH}"
export PKG_CONFIG_PATH="%{tde_prefix}/%{_lib}/pkgconfig"


%install -a
%find_lang %{tde_pkg}

# Fix desktop icon location
if [ -d "%{?buildroot}%{tde_prefix}/share/applnk" ]; then
  %__mkdir_p "%{?buildroot}%{tde_prefix}/share/applications/tde"
  %__mv -f "%{?buildroot}%{tde_prefix}/share/applnk/Games/Board/knights.desktop" "%{?buildroot}%{tde_prefix}/share/applications/tde"
  %__rm -r "%{buildroot}%{tde_prefix}/share/applnk"
fi


%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%{tde_prefix}/bin/knights
%{tde_prefix}/share/applications/tde/knights.desktop
%{tde_prefix}/share/apps/knights
%{tde_prefix}/share/doc/tde/HTML/*/knights
%{tde_prefix}/share/icons/hicolor/*/*/*.png
%{tde_prefix}/share/mimelnk/application/pgn.desktop
%{tde_prefix}/share/man/man1/*.1*

