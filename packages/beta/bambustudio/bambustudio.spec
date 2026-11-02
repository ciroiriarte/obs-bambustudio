#
# spec file for package bambustudio
#
# Community/unofficial build of Bambu Studio from upstream source.
#
# Dependency policy (see README "How the build works"):
#   * Libraries come from the target distribution wherever it ships a version
#     BambuStudio builds against.
#   * The rest (%%{deps_targets}: the bambulab wxWidgets fork, Boost, TBB, OCCT,
#     CGAL, OpenVDB and its Blosc/OpenEXR, libnoise) is built here from
#     upstream's own superbuild (deps/) as static archives inside the build
#     tree, linked into bambu-studio and discarded. Nothing of them is
#     installed, so they cannot clash with the distribution's packages.
#
# Upstream source: https://github.com/bambulab/BambuStudio (AGPL-3.0)
# Packaging:       https://github.com/ciroiriarte/obs-bambustudio
#

# Upstream tags are zero-padded (v02.08.02.61); RPM Version drops the padding.
%global upstream_ver   02.08.04.57
# bambulab/wxWidgets is consumed upstream as "GIT_TAG master"; pin the fork
# commit that was current when v%%{upstream_ver} was released.
%global wx_commit      7c74234803455026ec7287827bd545e5a8ed79b7
# Superbuild configuration. tools/gen_deps.py reads these two lines to compute
# which upstream tarballs become Source lines, so edit them only here and
# re-run the generator. DEP_BUILD_*=OFF / *_FOUND=ON select the system library.
%global deps_cmake_flags -DCMAKE_POLICY_VERSION_MINIMUM=3.5 -DDEP_WX_GTK3=ON -DDEP_BUILD_PNG=OFF -DDEP_BUILD_JPEG=OFF -DDEP_BUILD_TIFF=OFF -DDEP_BUILD_OPENSSL=OFF -DDEP_BUILD_GLFW=OFF -DDEP_BUILD_FREETYPE=OFF -DDEP_BUILD_GMP=OFF -DDEP_BUILD_MPFR=OFF -DDEP_BUILD_FFMPEG=OFF -DDEP_BUILD_LIBHARU=OFF -DEXPAT_FOUND=ON -DCURL_FOUND=ON
%global deps_targets   dep_wxWidgets dep_Boost dep_TBB dep_OCCT dep_CGAL dep_OpenVDB dep_libnoise
# LTO over the large static link needs far more memory than OBS workers have.
%global _lto_cflags    %{nil}

Name:           bambustudio
Version:        2.8.4.57
Release:        0
Summary:        Slicer for Bambu Lab and other FDM 3D printers
# Bundled, statically linked: wxWidgets fork (wxWindows), Boost (BSL-1.0),
# oneTBB (Apache-2.0), OCCT (LGPL-2.1-only WITH OCCT-exception-1.0),
# CGAL (GPL-3.0-or-later / LGPL-3.0-or-later), OpenVDB (MPL-2.0),
# Blosc (BSD-3-Clause), OpenEXR (BSD-3-Clause), libnoise (LGPL-2.1-or-later).
License:        AGPL-3.0-only AND BSL-1.0 AND Apache-2.0 AND GPL-3.0-or-later AND LGPL-3.0-or-later AND LGPL-2.1-or-later AND MPL-2.0 AND BSD-3-Clause
Group:          Productivity/Graphics/CAD
URL:            https://github.com/bambulab/BambuStudio
Source0:        https://github.com/bambulab/BambuStudio/archive/refs/tags/v%{upstream_ver}.tar.gz#/BambuStudio-%{upstream_ver}.tar.gz
Source1:        https://github.com/bambulab/wxWidgets/archive/%{wx_commit}.tar.gz#/wxWidgets-%{wx_commit}.tar.gz
Source2:        %{name}-rpmlintrc
# BEGIN generated deps sources (tools/gen_deps.py)
# sha256 dcb48bf43a672fa3de6a4b1de2c4c238709dad5893d1e097b8374ad84b1fc3b3
Source100:      https://github.com/tamasmeszaros/c-blosc/archive/refs/heads/v1.17.0_tm.zip#/dep__Blosc__v1.17.0_tm.zip
# sha256 4d27e9efed0f6f152dc28db6430b9d3dfb40c0345da7342eaa5a987dde57bd95
Source101:      https://github.com/boostorg/boost/releases/download/boost-1.84.0/boost-1.84.0.tar.gz#/dep__Boost__boost-1.84.0.tar.gz
# sha256 d7605e0a5a5ca17da7547592f6f6e4a59430a0bc861948974254d0de43eab4c0
Source102:      https://github.com/CGAL/cgal/archive/refs/tags/v5.4.zip#/dep__CGAL__v5.4.zip
# sha256 28334f0e98f1b1629799783e9b4d21e05349d89e695809d7e6dfa45ea43e1dbc
Source103:      https://github.com/Open-Cascade-SAS/OCCT/archive/refs/tags/V7_6_0.zip#/dep__OCCT__V7_6_0.zip
# sha256 0307a3d7e1fa1e77e9d84d7e9a8694583fbbbfd50bdc6884e2c96b8ef6b902de
Source104:      https://github.com/AcademySoftwareFoundation/openexr/archive/refs/tags/v2.5.5.zip#/dep__OpenEXR__v2.5.5.zip
# sha256 f353e7b99bd0cbfc27ac9082de51acf32a8bc0b3e21ff9661ecca6f205ec1d81
Source105:      https://github.com/tamasmeszaros/openvdb/archive/a68fd58d0e2b85f01adeb8b13d7555183ab10aa5.zip#/dep__OpenVDB__a68fd58d0e2b85f01adeb8b13d7555183ab10aa5.zip
# sha256 83ea786c964a384dd72534f9854b419716f412f9d43c0be88d41874763e7bb47
Source106:      https://github.com/oneapi-src/oneTBB/archive/refs/tags/v2021.5.0.zip#/dep__TBB__v2021.5.0.zip
# sha256 7aae3433e4c841a1b15ddf40dc995b3d32efb154b92b6796888002e275bff859
Source107:      https://github.com/bambulab/libnoise/archive/refs/tags/v1.0.0.zip#/dep__libnoise__v1.0.0.zip
# END generated deps sources
BuildRequires:  binutils
BuildRequires:  cmake >= 3.13
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  git-core
BuildRequires:  ninja
BuildRequires:  pkgconfig
BuildRequires:  unzip
# --- used by the bundled superbuild and the app ---
BuildRequires:  pkgconfig(bzip2)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(expat)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glu)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-base-1.0)
BuildRequires:  pkgconfig(gstreamer-video-1.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libsecret-1)
BuildRequires:  pkgconfig(libtiff-4)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(webkit2gtk-4.1)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(zlib)
# --- system libraries replacing upstream's bundled copies ---
BuildRequires:  cereal-devel
BuildRequires:  gmp-devel
BuildRequires:  mpfr-devel
BuildRequires:  pkgconfig(assimp)
BuildRequires:  pkgconfig(glew)
BuildRequires:  pkgconfig(glfw3)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(nlopt)
BuildRequires:  pkgconfig(opencv4)
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
Recommends:     gstreamer-plugins-base
Recommends:     gstreamer-plugins-good

%description
Bambu Studio is a feature-rich slicing software for FDM 3D printers. It
provides project-based workflows, optimized slicing algorithms and an
easy-to-use graphical interface. It ships printer, filament and process
profiles for Bambu Lab printers and many third-party machines, and can send
jobs to and monitor Bambu Lab printers on the network.

Bambu Studio is based on PrusaSlicer by Prusa Research, which is from Slic3r
by Alessandro Ranellucci and the RepRap community.

This is a community build; it is not provided or supported by Bambu Lab.
The optional proprietary "Bambu Network Plugin" (cloud/LAN printer control)
is downloaded by the application itself at runtime on user request.

%prep
%setup -q -n BambuStudio-%{upstream_ver}

# wxWidgets fork: a pinned tarball instead of an unpinned git clone of master.
# Its git submodules (png/jpeg/tiff/zlib/expat/catch) are unused: the recipe
# builds wx against the system libraries ("sys").
sed -i -e 's|GIT_REPOSITORY "https://github.com/bambulab/wxWidgets"|URL %{SOURCE1}|' \
       -e '/GIT_TAG master/d' deps/wxWidgets/wxWidgets.cmake
grep -q 'URL %{SOURCE1}' deps/wxWidgets/wxWidgets.cmake

# Pre-seed ExternalProject's download directory. download_files stored each
# bundled dependency as dep__<Dir>__<file>; ExternalProject expects it at
# <DEP_DOWNLOAD_DIR>/<Dir>/<file>, verifies upstream's SHA256 and skips the
# download (the build has no network).
for f in %{_sourcedir}/dep__*__*; do
    n=${f##*/dep__}
    d=${n%%%%__*}
    mkdir -p "deps-dl/$d"
    cp -p "$f" "deps-dl/$d/${n#*__}"
done

%build
%if 0%{?suse_version}
# Large OCCT/libslic3r/GUI translation units need ~2.5 GB each.
%limit_build -m 2500
%endif
NCPUS=%{?_smp_build_ncpus}%{!?_smp_build_ncpus:2}

# 1) Bundled dependencies: static, installed into the build tree only.
#    Built one at a time (upstream's advice); each one uses NCPUS jobs.
export CMAKE_BUILD_PARALLEL_LEVEL=$NCPUS
cmake -S deps -B deps/build -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DDESTDIR="$PWD/deps-destdir" \
    -DDEP_DOWNLOAD_DIR="$PWD/deps-dl" \
    %{deps_cmake_flags}
cmake --build deps/build -j1 --target %{deps_targets}
unset CMAKE_BUILD_PARALLEL_LEVEL

# 2) BambuStudio. Distribution flags, with reduced debug info to keep the
#    static link within OBS worker memory. --exclude-libs keeps the bundled
#    archives' symbols out of the dynamic symbol table, so they can never
#    interpose on (or be interposed by) a distribution copy of the same
#    library loaded indirectly at runtime.
export CFLAGS="$(echo "%{optflags}" | sed 's/ -g / -g1 /; s/ -g$/ -g1/')"
export CXXFLAGS="$CFLAGS"
export LDFLAGS="-Wl,--exclude-libs,ALL"
cmake -S . -B build -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_PREFIX_PATH="$PWD/deps-destdir/usr/local" \
    -DOpenGL_GL_PREFERENCE=GLVND \
    -DSLIC3R_STATIC=ON \
    -DSLIC3R_STATIC_EXCLUDE_CURL=ON \
    -DSLIC3R_STATIC_EXCLUDE_GLEW=ON \
    -DSLIC3R_GTK=3 \
    -DSLIC3R_FHS=ON \
    -DSLIC3R_BUILD_TESTS=OFF \
    -DBBL_RELEASE_TO_PUBLIC=1 \
    -DBBL_INTERNAL_TESTING=0 \
    -DFLATPAK=ON
cmake --build build -j $NCPUS

%install
DESTDIR=%{buildroot} cmake --install build
%if 0%{?suse_version}
%fdupes %{buildroot}%{_datadir}/BambuStudio
%endif

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/BambuStudio.desktop
# The bundled libraries must be linked in statically and stay private.
bin=%{buildroot}%{_bindir}/bambu-studio
if readelf -d "$bin" | grep -E 'NEEDED.*(libtbb|libboost|libTK|libwx_|libopenvdb|libnoise|libblosc|libHalf|libIlm)'; then
    echo "error: bambu-studio links a system copy of a bundled library" >&2
    exit 1
fi
if nm -DC --defined-only "$bin" | grep -E ' (tbb|boost|openvdb|CGAL|noise)::| wx[A-Z]'; then
    echo "error: bambu-studio exports symbols of a bundled library" >&2
    exit 1
fi

%files
%license LICENSE
%doc README.md
%{_bindir}/bambu-studio
%{_datadir}/BambuStudio
%{_datadir}/applications/BambuStudio.desktop
%{_datadir}/icons/hicolor/*/apps/BambuStudio.png

%changelog
