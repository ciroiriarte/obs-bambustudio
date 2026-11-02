#
# spec file for package bambustudio
#
# Community/unofficial build of Bambu Studio from upstream source. Third-party
# libraries are linked statically from bambustudio-deps (upstream's own
# dependency superbuild); GTK, WebKitGTK, GStreamer, OpenSSL and FFmpeg come
# from the distribution.
#
# Upstream source: https://github.com/bambulab/BambuStudio (AGPL-3.0)
# Packaging:       https://github.com/ciroiriarte/obs-bambustudio
#

# Upstream tags are zero-padded (v02.08.02.61); RPM Version drops the padding.
%global upstream_ver   02.08.02.61
%global deps_prefix    /opt/bambustudio-deps
# LTO over a ~600k-line static link needs far more memory than OBS workers have.
%global _lto_cflags    %{nil}

Name:           bambustudio
Version:        2.8.2.61
Release:        0
Summary:        Slicer for Bambu Lab and other FDM 3D printers
License:        AGPL-3.0-only
Group:          Productivity/Graphics/CAD
URL:            https://github.com/bambulab/BambuStudio
Source0:        https://github.com/bambulab/BambuStudio/archive/refs/tags/v%{upstream_ver}.tar.gz#/BambuStudio-%{upstream_ver}.tar.gz
Source1:        %{name}-rpmlintrc
BuildRequires:  bambustudio-deps = %{version}
BuildRequires:  cmake >= 3.13
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  git-core
BuildRequires:  ninja
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(bzip2)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glu)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-base-1.0)
BuildRequires:  pkgconfig(gstreamer-video-1.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(libsecret-1)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(webkit2gtk-4.1)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(zlib)
%if 0%{?suse_version}
BuildRequires:  fdupes
BuildRequires:  memory-constraints
# Several FFmpeg majors coexist on openSUSE; upstream targets FFmpeg 7.
BuildRequires:  ffmpeg-7-libavcodec-devel
BuildRequires:  ffmpeg-7-libavutil-devel
BuildRequires:  ffmpeg-7-libswscale-devel
%else
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswscale)
%endif
# Printer camera live view goes through GStreamer.
Recommends:     gstreamer-plugins-good
Recommends:     gstreamer-plugins-base

%description
Bambu Studio is a cutting-edge, feature-rich slicing software for FDM 3D
printers. It provides project-based workflows, systematically optimized
slicing algorithms and an easy-to-use graphical interface. It ships printer,
filament and process profiles for Bambu Lab printers and many third-party
machines, and can send jobs to and monitor Bambu Lab printers on the network.

Bambu Studio is based on PrusaSlicer by Prusa Research, which is from Slic3r
by Alessandro Ranellucci and the RepRap community.

This is a community build; it is not provided or supported by Bambu Lab.
The optional proprietary "Bambu Network Plugin" (cloud/LAN printer control)
is downloaded by the application itself at runtime on user request.

%prep
%setup -q -n BambuStudio-%{upstream_ver}

%build
%if 0%{?suse_version}
# Large libslic3r/GUI translation units need ~2.5 GB each.
%limit_build -m 2500
%endif
# Distribution flags, with reduced debug info to keep the static link within
# OBS worker memory.
export CFLAGS="$(echo "%{optflags}" | sed 's/ -g / -g1 /; s/ -g$/ -g1/')"
export CXXFLAGS="$CFLAGS"
cmake -S . -B build -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_PREFIX_PATH=%{deps_prefix}/usr/local \
    -DOpenGL_GL_PREFERENCE=GLVND \
    -DSLIC3R_STATIC=ON \
    -DSLIC3R_GTK=3 \
    -DSLIC3R_FHS=ON \
    -DSLIC3R_BUILD_TESTS=OFF \
    -DBBL_RELEASE_TO_PUBLIC=1 \
    -DBBL_INTERNAL_TESTING=0 \
    -DFLATPAK=ON
cmake --build build -j %{?_smp_build_ncpus}%{!?_smp_build_ncpus:2}

%install
DESTDIR=%{buildroot} cmake --install build
%if 0%{?suse_version}
%fdupes %{buildroot}%{_datadir}/BambuStudio
%endif

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/BambuStudio.desktop

%files
%license LICENSE
%doc README.md
%{_bindir}/bambu-studio
%{_datadir}/BambuStudio
%{_datadir}/applications/BambuStudio.desktop
%{_datadir}/icons/hicolor/*/apps/BambuStudio.png

%changelog
