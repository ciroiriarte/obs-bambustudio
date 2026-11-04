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
%global deps_targets   dep_wxWidgets dep_Boost dep_TBB dep_OCCT dep_CGAL dep_OpenVDB dep_libnoise dep_OpenMeshCraft
# device_page web frontend (src/slic3r/GUI/DeviceWeb): built with the distro
# Node.js, pnpm from its npm tarball, and the npm packages from a vendored pnpm
# store (GitHub release asset of the packaging repo). tools/vendor_web.py sets
# both values from upstream's PNPM_VERSION and pnpm-lock.yaml.
%global pnpm_version   10.12.1
%global web_store      b6f4988b0e50
# LTO over the large static link needs far more memory than OBS workers have.
%global _lto_cflags    %{nil}

Name:           bambustudio
Version:        2.8.4.57
Release:        0
Summary:        Slicer for Bambu Lab and other FDM 3D printers
# Bundled, statically linked: wxWidgets fork (wxWindows), Boost (BSL-1.0),
# oneTBB (Apache-2.0), OCCT (LGPL-2.1-only WITH OCCT-exception-1.0),
# CGAL (GPL-3.0-or-later / LGPL-3.0-or-later), OpenVDB (MPL-2.0),
# Blosc (BSD-3-Clause), OpenEXR (BSD-3-Clause), libnoise (LGPL-2.1-or-later),
# OpenMeshCraft (GPL-3.0-only).
License:        AGPL-3.0-only AND GPL-3.0-only AND BSL-1.0 AND Apache-2.0 AND GPL-3.0-or-later AND LGPL-3.0-or-later AND LGPL-2.1-or-later AND MPL-2.0 AND BSD-3-Clause
Group:          Productivity/Graphics/CAD
URL:            https://github.com/bambulab/BambuStudio
Source0:        https://github.com/bambulab/BambuStudio/archive/refs/tags/v%{upstream_ver}.tar.gz#/BambuStudio-%{upstream_ver}.tar.gz
Source1:        https://github.com/bambulab/wxWidgets/archive/%{wx_commit}.tar.gz#/wxWidgets-%{wx_commit}.tar.gz
Source2:        %{name}-rpmlintrc
Source3:        https://registry.npmjs.org/pnpm/-/pnpm-%{pnpm_version}.tgz
Source4:        https://github.com/ciroiriarte/obs-bambustudio/releases/download/web-store-%{web_store}/device-page-store-%{web_store}.tar.zst
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
# sha256 632cd806ce932d6a1d76df0e86ecf8bfc22480e76f80a638a28474f5262e2b9e
Source105:      https://github.com/bambulab/OpenMeshCraft/archive/0e8d12c3df54804393593ab5d86c05caa340cbee.zip#/dep__OpenMeshCraft__0e8d12c3df54804393593ab5d86c05caa340cbee.zip
# sha256 f353e7b99bd0cbfc27ac9082de51acf32a8bc0b3e21ff9661ecca6f205ec1d81
Source106:      https://github.com/tamasmeszaros/openvdb/archive/a68fd58d0e2b85f01adeb8b13d7555183ab10aa5.zip#/dep__OpenVDB__a68fd58d0e2b85f01adeb8b13d7555183ab10aa5.zip
# sha256 83ea786c964a384dd72534f9854b419716f412f9d43c0be88d41874763e7bb47
Source107:      https://github.com/oneapi-src/oneTBB/archive/refs/tags/v2021.5.0.zip#/dep__TBB__v2021.5.0.zip
# sha256 7aae3433e4c841a1b15ddf40dc995b3d32efb154b92b6796888002e275bff859
Source108:      https://github.com/bambulab/libnoise/archive/refs/tags/v1.0.0.zip#/dep__libnoise__v1.0.0.zip
# nested download in deps/OpenMeshCraft, sha256 41d12f1fc8e18606f39312681c6e1b957a4746ed97676c576e23e73554c6a662
Source109:      https://gitlab.com/libeigen/eigen/-/archive/68f4e58cfacc686583d16cff90361f0b43bc2c1b/eigen-68f4e58cfacc686583d16cff90361f0b43bc2c1b.zip#/nested__OpenMeshCraft__eigen-68f4e58cfacc686583d16cff90361f0b43bc2c1b.zip
# nested download in deps/OpenMeshCraft, sha256 29d0c510018d9bdaa5fbecaf95c2eaa616027d568e4a631d363b27620de4e07b
Source110:      https://github.com/greg7mdp/parallel-hashmap/archive/154c63489e84d5569d3b466342a2ae8fd99e4734.zip#/nested__OpenMeshCraft__154c63489e84d5569d3b466342a2ae8fd99e4734.zip
# nested download in deps/OpenMeshCraft, sha256 fe22388fb9435dcefa66c8189d4a8fbd8d968fda3a3dc4f578f78a3dd201c68e
Source111:      https://github.com/oneapi-src/oneTBB/archive/d75ea937f7e480bd7775d7dab224e0b38451bb40.zip#/nested__OpenMeshCraft__d75ea937f7e480bd7775d7dab224e0b38451bb40.zip
# nested download in deps/OpenMeshCraft, sha256 d368f9c39a33a3aef800f5be372ec1df1c12ad57ada1f60adc62f24c0e348469
Source112:      https://github.com/fmtlib/fmt/archive/refs/tags/10.2.1.zip#/nested__OpenMeshCraft__10.2.1.zip
# URL@@file map for %prep: nested downloads are rewritten to file:// Sources
%global nested_fetches https://gitlab.com/libeigen/eigen/-/archive/68f4e58cfacc686583d16cff90361f0b43bc2c1b/eigen-68f4e58cfacc686583d16cff90361f0b43bc2c1b.zip@@nested__OpenMeshCraft__eigen-68f4e58cfacc686583d16cff90361f0b43bc2c1b.zip https://github.com/greg7mdp/parallel-hashmap/archive/154c63489e84d5569d3b466342a2ae8fd99e4734.zip@@nested__OpenMeshCraft__154c63489e84d5569d3b466342a2ae8fd99e4734.zip https://github.com/oneapi-src/oneTBB/archive/d75ea937f7e480bd7775d7dab224e0b38451bb40.zip@@nested__OpenMeshCraft__d75ea937f7e480bd7775d7dab224e0b38451bb40.zip https://github.com/fmtlib/fmt/archive/refs/tags/10.2.1.zip@@nested__OpenMeshCraft__10.2.1.zip
# END generated deps sources
BuildRequires:  binutils
BuildRequires:  cmake >= 3.13
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  git-core
BuildRequires:  ninja
BuildRequires:  nodejs >= 22
BuildRequires:  pkgconfig
BuildRequires:  unzip
BuildRequires:  zstd
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
BuildRequires:  libharu-devel
BuildRequires:  libquadmath-devel
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

# System libharu installs its headers flat (%{_includedir}/hpdf*.h); upstream's
# bundled copy uses include/hpdf/. Rewrite <hpdf/...> includes to the flat form.
files=$(grep -rlE '#include *[<"]hpdf/' src)
test -n "$files"
sed -i -E 's|(#include *[<"])hpdf/|\1|' $files
if grep -rqE '#include *[<"]hpdf/' src; then
    echo "error: unrewritten hpdf/ include" >&2
    exit 1
fi

# System cereal exports only the cereal::cereal target; upstream links the
# bare name "cereal" (defined by its bundled copy), which CMake would turn into
# -lcereal. cereal is header-only: forward the bare name to the system target.
sed -i '/^find_package(cereal REQUIRED)$/a\
if(NOT TARGET cereal)\
    add_library(cereal INTERFACE)\
    target_link_libraries(cereal INTERFACE cereal::cereal)\
endif()' CMakeLists.txt
grep -q 'target_link_libraries(cereal INTERFACE cereal::cereal)' CMakeLists.txt

# Upstream links its bundled monolithic opencv_world; the distribution ships
# per-module libraries. Find and link the modules the code uses.
sed -i -e 's/^find_package(OpenCV REQUIRED core)$/find_package(OpenCV REQUIRED core imgproc imgcodecs)/' \
       -e 's/^\( *\)opencv_world$/\1${OpenCV_LIBS}/' src/libslic3r/CMakeLists.txt
grep -q '^find_package(OpenCV REQUIRED core imgproc imgcodecs)$' src/libslic3r/CMakeLists.txt
grep -q '^ *${OpenCV_LIBS}$' src/libslic3r/CMakeLists.txt
if grep -q 'opencv_world' src/libslic3r/CMakeLists.txt; then
    echo "error: opencv_world still linked" >&2
    exit 1
fi

# Nothing calls OSMesa directly (GLFW dlopens it for its OSMesa context API)
# and current Mesa no longer ships libOSMesa: drop the hard link.
sed -i 's/^\( *target_link_libraries(libslic3r_gui ${DBUS_LIBRARIES}\) OSMesa)$/\1)/' src/slic3r/CMakeLists.txt
if grep -qw 'OSMesa' src/slic3r/CMakeLists.txt; then
    echo "error: OSMesa still linked" >&2
    exit 1
fi

# OpenGL loading with the distribution's GLEW and GLFW:
# - Upstream's bundled GLEW is built with GLEW_EGL (its wxWidgets uses EGL on
#   GTK3); the distro GLEW is GLX-only, so glewInit() fails on EGL contexts
#   with GLEW_ERROR_NO_GLX_DISPLAY. glewContextInit() loads core GL and the
#   extensions without the window-system check (no GLX/EGL GLEW API is used).
# - The CLI thumbnail renderer requests an OpenGL context whose version is
#   GLFW's own library version (3.3 when bundled, "3.5" with system GLFW 3.5:
#   invalid) and forces OSMesa, which current Mesa no longer ships. Request
#   OpenGL 3.3 compatibility on the native context API instead.
files=$(grep -rl 'glewInit()' src)
test -n "$files"
sed -i 's/\bglewInit()/glewContextInit()/' $files
sed -i -e 's/glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, gl_major);/glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);/' \
       -e 's/glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, gl_minor);/glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);/' \
       -e '/glfwWindowHint(GLFW_CONTEXT_CREATION_API, GLFW_OSMESA_CONTEXT_API);/d' src/BambuStudio.cpp
grep -q 'glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);' src/BambuStudio.cpp
if grep -rqE 'glewInit\(\)|GLFW_CONTEXT_VERSION_MAJOR, gl_major|GLFW_CONTEXT_VERSION_MINOR, gl_minor|GLFW_OSMESA_CONTEXT_API' src; then
    echo "error: unpatched GLEW/GLFW context setup" >&2
    exit 1
fi

# Bambu's closed network plugin (libbambu_networking.so, downloaded at run
# time) carries its own OpenSSL, whose built-in CA path does not exist on
# this distribution; it trusts SSL_CERT_FILE. Upstream's static builds set
# that variable from a list of distro CA bundles (Http.cpp, only with
# OPENSSL_CERT_OVERRIDE); this build links the system OpenSSL, so nothing
# sets it, and every cloud call fails verification (curl error 60: no
# printer list, no printers to send to). Set it at startup unless the user
# already did.
sed -i '/^int main(int argc, char \*\*argv)$/,/^}$/ s|^    std::set_new_handler(bbl_out_of_memory_handler);$|&\
    if (!::getenv("SSL_CERT_FILE"))\
        for (const char *ca : {"/etc/pki/tls/certs/ca-bundle.crt", "/etc/ssl/certs/ca-certificates.crt",\
                               "/etc/ssl/ca-bundle.pem"})\
            if (boost::filesystem::exists(ca)) { ::setenv("SSL_CERT_FILE", ca, 0); break; }|' src/BambuStudio.cpp
if ! grep -q 'setenv("SSL_CERT_FILE"' src/BambuStudio.cpp; then
    echo "error: SSL_CERT_FILE startup default not applied" >&2
    exit 1
fi

# Downloads a bundled recipe performs itself (e.g. OpenMeshCraft fetches
# Eigen/fmt/... from its generated prepare_source.cmake): point each URL at its
# local Source via file://; upstream's SHA256 check still applies.
for m in %{nested_fetches}; do
    url=${m%%%%@@*}
    grep -rlF "$url" deps | xargs -r sed -i "s|$url|file://%{_sourcedir}/${m#*@@}|"
    if grep -rqF "$url" deps; then
        echo "error: could not redirect $url" >&2
        exit 1
    fi
done

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

# device_page web frontend, offline. Upstream's CMake looks for node and pnpm
# in ../node-cache/node-v<NODE_VERSION>-linux-<arch>/bin and downloads them if
# missing; seed that directory with the distro node and an offline pnpm.
node_ver=$(sed -n 's/.*set(NODE_VERSION "\([^"]*\)").*/\1/p' src/slic3r/GUI/DeviceWeb/CMakeLists.txt)
test -n "$node_ver"
case "%{_arch}" in aarch64) node_arch=arm64 ;; *) node_arch=x64 ;; esac
nodecache=$(dirname "$PWD")/node-cache
bindir=$nodecache/node-v$node_ver-linux-$node_arch/bin
mkdir -p "$bindir" "$nodecache/pnpm"
tar -C "$nodecache/pnpm" --strip-components=1 -xzf %{SOURCE3}
tar -C "$nodecache" --zstd -xf %{SOURCE4}
ln -s "$(command -v node)" "$bindir/node"
cat > "$bindir/pnpm" <<EOF
#!/bin/sh
# Offline pnpm for the package build: installs only from the vendored store.
if [ "\$1" = install ]; then
    exec node "$nodecache/pnpm/bin/pnpm.cjs" install --offline --frozen-lockfile --store-dir "$nodecache/pnpm-store"
fi
exec node "$nodecache/pnpm/bin/pnpm.cjs" "\$@"
EOF
chmod +x "$bindir/pnpm"

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
# pnpm/vite: non-interactive, no update checks (no network)
export CI=1 npm_config_update_notifier=false
cmake -S . -B build -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_SKIP_INSTALL_RPATH=ON \
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
# The vendored mcut (src/mcut) installs its development files and docs into
# the prefix; it is linked statically and nothing else needs them.
rm -r %{buildroot}%{_includedir}/mcut
rm %{buildroot}%{_prefix}/LICENSE.txt %{buildroot}%{_prefix}/README.md
rmdir --ignore-fail-on-non-empty %{buildroot}%{_includedir}
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
