#
# spec file for package bambustudio-deps
#
# Build-only helper for bambustudio: upstream's static dependency superbuild
# (deps/CMakeLists.txt) built offline. Installed to %%{deps_prefix} and
# consumed by bambustudio.spec via CMAKE_PREFIX_PATH; it is publish-disabled
# in the OBS project meta, so end users never see it. Everything it ships is a
# static library or header (FFmpeg/OpenSSL come from the distribution), so
# bambustudio has no runtime dependency on this package.
#
# Upstream source: https://github.com/bambulab/BambuStudio (AGPL-3.0)
# Packaging:       https://github.com/ciroiriarte/obs-bambustudio
#

# Static archives and headers only: no debuginfo, and no brp post-processing
# (stripping/relinking static archives from 20+ projects is slow and pointless
# for a build-only package).
%global debug_package %{nil}
%global __os_install_post %{nil}

# Upstream tags are zero-padded (v02.08.02.61); RPM Version drops the padding.
%global upstream_ver   02.08.02.61
# bambulab/wxWidgets is consumed upstream as "GIT_TAG master"; pin the fork
# commit that was current when v%%{upstream_ver} was released.
%global wx_commit      a9d946902685b9946d8775f07d2a73a9b5bef394
%global deps_prefix    /opt/bambustudio-deps
# Flags for deps/CMakeLists.txt. tools/gen_deps.py reads this line to compute
# which tarballs the superbuild downloads, so edit flags only here.
#   FFMPEG off:  linked from the distribution (libavcodec), see bambustudio.spec
#   OPENSSL off: use the maintained system OpenSSL 3, not the bundled 1.1.1k
%global deps_cmake_flags -DCMAKE_POLICY_VERSION_MINIMUM=3.5 -DDEP_WX_GTK3=ON -DDEP_BUILD_FFMPEG=OFF -DDEP_BUILD_OPENSSL=OFF

Name:           bambustudio-deps
Version:        2.8.2.61
Release:        0
Summary:        Static build dependencies for BambuStudio (build-only)
License:        AGPL-3.0-only AND BSD-3-Clause AND BSL-1.0 AND Apache-2.0 AND MIT AND LGPL-3.0-or-later AND LGPL-2.1-only AND MPL-2.0 AND Zlib AND libpng-2.0
URL:            https://github.com/bambulab/BambuStudio
Source0:        https://github.com/bambulab/BambuStudio/archive/refs/tags/v%{upstream_ver}.tar.gz#/BambuStudio-%{upstream_ver}.tar.gz
Source1:        https://github.com/bambulab/wxWidgets/archive/%{wx_commit}.tar.gz#/wxWidgets-%{wx_commit}.tar.gz
Source2:        %{name}-rpmlintrc
# BEGIN generated deps sources (tools/gen_deps.py)
# sha256 66dfbaee288f2bc43172440a55d0235dfc7bf885dda6435c038e8000e79582cb
Source100:   https://github.com/assimp/assimp/archive/refs/tags/v5.4.3.tar.gz#/dep__Assimp__v5.4.3.tar.gz
# sha256 dcb48bf43a672fa3de6a4b1de2c4c238709dad5893d1e097b8374ad84b1fc3b3
Source101:   https://github.com/tamasmeszaros/c-blosc/archive/refs/heads/v1.17.0_tm.zip#/dep__Blosc__v1.17.0_tm.zip
# sha256 4d27e9efed0f6f152dc28db6430b9d3dfb40c0345da7342eaa5a987dde57bd95
Source102:   https://github.com/boostorg/boost/releases/download/boost-1.84.0/boost-1.84.0.tar.gz#/dep__Boost__boost-1.84.0.tar.gz
# sha256 d7605e0a5a5ca17da7547592f6f6e4a59430a0bc861948974254d0de43eab4c0
Source103:   https://github.com/CGAL/cgal/archive/refs/tags/v5.4.zip#/dep__CGAL__v5.4.zip
# sha256 a63ae025bb0a14f119e73250f2c923f4bf89aa93b8d4fafa4a9f5353a96a765a
Source104:   https://github.com/curl/curl/archive/refs/tags/curl-7_75_0.zip#/dep__CURL__curl-7_75_0.zip
# sha256 71642cb54658e98c8f07a0f0d08bf9766f1c3771496936f6014169d3726d9657
Source105:   https://github.com/USCiLab/cereal/archive/refs/tags/v1.3.0.zip#/dep__Cereal__v1.3.0.zip
# sha256 0e72cae32751598d126cfd4bceda909f646b7231ab8c52e28abb686c20a2bea1
Source106:   https://github.com/freetype/freetype/archive/refs/tags/VER-2-12-1.tar.gz#/dep__FREETYPE__VER-2-12-1.tar.gz
# sha256 e02d956935e5b9fb4abf90e2c2e07c9a0526d7eacae8ee5353484c69a2a76cd0
Source107:   https://github.com/glfw/glfw/archive/refs/tags/3.3.7.zip#/dep__GLFW__3.3.7.zip
# sha256 705ae57ee2014b2c6fc0f572c85ee43276b99b6b256ee16c1a9d3a8c4e3609d5
Source108:   https://github.com/bambulab/gmp/archive/refs/tags/6.2.1.tar.gz#/dep__GMP__6.2.1.tar.gz
# sha256 d6d99e693366bc03897677650e8b2dfa76b5d6c54e2c9e70c03f0af821b0a52f
Source109:   https://github.com/libjpeg-turbo/libjpeg-turbo/archive/refs/tags/3.0.1.zip#/dep__JPEG__3.0.1.zip
# sha256 cf4f4b2d80abb79e820e78c8077b6725bbbb4e8f41896783c899087be0e94068
Source110:   https://www.mpfr.org/mpfr-3.1.6/mpfr-3.1.6.tar.bz2#/dep__MPFR__mpfr-3.1.6.tar.bz2
# sha256 c6dd7a5701fff8ad5ebb45a3dc8e757e61d52658de3918e38bab233e7fd3b4ae
Source111:   https://github.com/stevengj/nlopt/archive/v2.5.0.tar.gz#/dep__NLopt__v2.5.0.tar.gz
# sha256 28334f0e98f1b1629799783e9b4d21e05349d89e695809d7e6dfa45ea43e1dbc
Source112:   https://github.com/Open-Cascade-SAS/OCCT/archive/refs/tags/V7_6_0.zip#/dep__OCCT__V7_6_0.zip
# sha256 51afe0db79af8386e2027d56d685177135581e0ee82ade9d7f2caff8deab5ec5
Source113:   https://github.com/floriankirsch/OpenCSG/archive/refs/tags/opencsg-1-4-2-release.zip#/dep__OpenCSG__opencsg-1-4-2-release.zip
# sha256 1ec1cba65f9f20fe5a41fda1586e01c70ea0c9a6d7b67c9e13edf0cfe2239277
Source114:   https://github.com/opencv/opencv/archive/refs/tags/4.6.0.tar.gz#/dep__OpenCV__4.6.0.tar.gz
# sha256 0307a3d7e1fa1e77e9d84d7e9a8694583fbbbfd50bdc6884e2c96b8ef6b902de
Source115:   https://github.com/AcademySoftwareFoundation/openexr/archive/refs/tags/v2.5.5.zip#/dep__OpenEXR__v2.5.5.zip
# sha256 f353e7b99bd0cbfc27ac9082de51acf32a8bc0b3e21ff9661ecca6f205ec1d81
Source116:   https://github.com/tamasmeszaros/openvdb/archive/a68fd58d0e2b85f01adeb8b13d7555183ab10aa5.zip#/dep__OpenVDB__a68fd58d0e2b85f01adeb8b13d7555183ab10aa5.zip
# sha256 3d22d46c566b1761a0e15ea397589b3a5f36ac09b7c785382e6470156c04247f
Source117:   https://github.com/glennrp/libpng/archive/refs/tags/v1.6.35.zip#/dep__PNG__v1.6.35.zip
# sha256 5287f5edd6a0372588f5d6640799086a4033d89d19711023ef8229dd9301d69b
Source118:   https://github.com/qhull/qhull/archive/v8.0.1.zip#/dep__Qhull__v8.0.1.zip
# sha256 83ea786c964a384dd72534f9854b419716f412f9d43c0be88d41874763e7bb47
Source119:   https://github.com/oneapi-src/oneTBB/archive/refs/tags/v2021.5.0.zip#/dep__TBB__v2021.5.0.zip
# sha256 6f3dbed9d2ecfed33c7192b5c01884078970657fa21b4ad28e3cdf3438eb2419
Source120:   https://download.osgeo.org/libtiff/tiff-4.1.0.zip#/dep__TIFF__tiff-4.1.0.zip
# sha256 7aae3433e4c841a1b15ddf40dc995b3d32efb154b92b6796888002e275bff859
Source121:   https://github.com/bambulab/libnoise/archive/refs/tags/v1.0.0.zip#/dep__libnoise__v1.0.0.zip
# END generated deps sources
# The .pc / CMake files under %%{deps_prefix} must not leak pkgconfig()/cmake()
# provides into the build root of other packages, and nothing here is needed
# at runtime.
AutoReqProv:    no
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  cmake >= 3.13
BuildRequires:  extra-cmake-modules
BuildRequires:  gcc-c++
BuildRequires:  git-core
BuildRequires:  libtool
BuildRequires:  m4
BuildRequires:  nasm
BuildRequires:  ninja
BuildRequires:  perl
BuildRequires:  pkgconfig
BuildRequires:  texinfo
BuildRequires:  unzip
BuildRequires:  wayland-protocols-devel
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
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(webkit2gtk-4.1)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(zlib)
%if 0%{?suse_version}
BuildRequires:  memory-constraints
%endif

%description
Static libraries and headers of the third-party dependencies BambuStudio
builds against (Boost, TBB, OpenVDB, CGAL, OpenCASCADE, OpenCV, the bambulab
wxWidgets fork and others), built from upstream's own dependency recipe so
the slicer links the exact versions and patches upstream tests with.

This is a build-time helper for the bambustudio package and is not meant to
be installed by end users.

%prep
%setup -q -n BambuStudio-%{upstream_ver}

# wxWidgets fork: a pinned tarball instead of an unpinned git clone of master.
# The fork's git submodules (png/jpeg/tiff/zlib/expat/catch) are unused: the
# recipe builds wx against the libraries from this superbuild ("sys").
sed -i -e 's|GIT_REPOSITORY "https://github.com/bambulab/wxWidgets"|URL %{SOURCE1}|' \
       -e '/GIT_TAG master/d' deps/wxWidgets/wxWidgets.cmake
grep -q 'URL %{SOURCE1}' deps/wxWidgets/wxWidgets.cmake

# Pre-seed ExternalProject's download directory. Each dependency tarball was
# stored by download_files as dep__<Dir>__<file>; ExternalProject expects it at
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
# OCCT/OpenCV/Boost translation units need ~1.5 GB each.
%limit_build -m 1500
%endif
# Read by deps/CMakeLists.txt as the per-dependency job count.
export CMAKE_BUILD_PARALLEL_LEVEL=%{?_smp_build_ncpus}%{!?_smp_build_ncpus:2}
cmake -S deps -B deps/build -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DDESTDIR="$PWD/destdir" \
    -DDEP_DOWNLOAD_DIR="$PWD/deps-dl" \
    %{deps_cmake_flags}
# One dependency at a time; each one builds in parallel internally
# (upstream's recommendation, and it keeps peak memory predictable).
cmake --build deps/build -j1

%install
mkdir -p %{buildroot}%{deps_prefix}
cp -a destdir/usr %{buildroot}%{deps_prefix}/
# Relocate the build-time prefix baked into wx-config, CMake package configs,
# pkg-config and libtool files.
grep -rlI "$PWD/destdir" %{buildroot}%{deps_prefix} \
    | xargs -r sed -i "s|$PWD/destdir|%{deps_prefix}|g"
# Fail loudly if any text file still points into the build tree.
if grep -rlI "$PWD" %{buildroot}%{deps_prefix}; then
    echo "error: build-tree paths left in the files above" >&2
    exit 1
fi

%files
%{deps_prefix}

%changelog
