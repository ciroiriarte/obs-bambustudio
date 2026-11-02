# obs-bambustudio — Bambu Studio packages for Linux distributions

[![upstream bump](https://github.com/ciroiriarte/obs-bambustudio/actions/workflows/upstream-bump.yml/badge.svg)](https://github.com/ciroiriarte/obs-bambustudio/actions/workflows/upstream-bump.yml)

Community/**unofficial** native packages of [Bambu Studio](https://github.com/bambulab/BambuStudio),
the 3D printing slicer, built **from upstream source** on the
[openSUSE Build Service](https://build.opensuse.org/project/show/home:ciriarte:bambustudio).
New upstream stable releases are picked up and rebuilt automatically.

> Bambu Studio and Bambu Lab are trademarks of their owner. This project is
> community-maintained and **not endorsed or supported by Bambu Lab**.
> Bambu Studio is licensed AGPL-3.0; so is this packaging.

- **OBS project:** `home:ciriarte:bambustudio`
- **Upstream:** https://github.com/bambulab/BambuStudio (stable releases only;
  "Public Beta" pre-releases are skipped)

## Supported targets

| Distro | `REPO` token | Arch | Status |
|--------|--------------|------|--------|
| openSUSE Slowroll | `openSUSE_Slowroll` | x86_64 | primary target |
| openSUSE Tumbleweed / Leap 16.0 | — | — | planned |
| Rocky Linux 9 / 10 | — | — | planned |
| Ubuntu 24.04 / Debian 13 | — | — | planned (needs `debian.*` recipe) |

OBS publishes Slowroll for x86_64 only.

## Install

### openSUSE (zypper)

```sh
REPO=openSUSE_Slowroll
BASE="https://download.opensuse.org/repositories/home:/ciriarte:/bambustudio/$REPO"
sudo zypper addrepo -f "$BASE/home:ciriarte:bambustudio.repo"
sudo zypper --gpg-auto-import-keys refresh
sudo zypper install bambustudio
```

Run it with `bambu-studio` or from the desktop menu.

### Printer camera / live view

Live view uses GStreamer and FFmpeg's `libavcodec`. openSUSE's own FFmpeg
build omits patent-encumbered decoders such as H.264, so camera streams may not
decode. If so, install the full codecs from [Packman](https://en.opensuse.org/Additional_package_repositories#Packman)
(`libavcodec61` / `gstreamer-plugins-libav`). Slicing and printing are unaffected.

### Bambu Network Plugin

Cloud/LAN printer control relies on Bambu Lab's proprietary network plugin.
It is **not** part of this package; Bambu Studio offers to download it on first
use, as on any other platform.

## How the build works

### Dependency policy

Libraries come from the **target distribution** wherever it ships a version
Bambu Studio builds against: GTK3, WebKitGTK 4.1, GStreamer, OpenSSL, curl,
FFmpeg 7, OpenCV, assimp, GLEW, GLFW, NLopt, cereal, GMP/MPFR, freetype,
libpng/libjpeg/libtiff/expat, zlib.

Only these are **bundled**, because the distributions cannot provide a usable
version:

| Bundled | Why |
|---------|-----|
| wxWidgets (bambulab fork) | Bambu Lab's patched fork; distributions ship stock 3.2 |
| Boost 1.84 | current Boost (1.87+) removed `asio::io_service`, still used upstream |
| OCCT 7.6, CGAL 5.4, OpenVDB 8.2 (+Blosc, OpenEXR) | API moved on in the distro versions; upstream pins/patches these |
| TBB 2021.5 | required statically by the static Boost/OpenVDB build |
| libnoise (bambulab fork) | not packaged by distributions |

### Bundled libraries never touch the system

They are built from upstream's own superbuild (`deps/CMakeLists.txt`) as
**static archives inside the build directory**, linked into `bambu-studio`
and discarded with the build tree. The RPM ships only the binary and
`/usr/share/BambuStudio`: no `.so`, `.a`, headers or `Provides:` for any
bundled library, so there is nothing to conflict with the distribution's
`libboost_*`, `libtbb`, `occt` or wxWidgets packages.

The binary is linked with `-Wl,--exclude-libs,ALL`, so bundled symbols are not
exported and cannot interpose on (or be interposed by) a distribution copy of
the same library that a system dependency loads at runtime. `%check` fails the
build if `bambu-studio` dynamically links or exports any bundled library.

### Building offline on OBS

OBS build workers have **no network**, but the superbuild downloads its tarballs
at build time. So:

1. `tools/gen_deps.py` configures upstream's superbuild (configure only) with
   the spec's `%deps_cmake_flags`, asks ninja for a dry run of `%deps_targets`
   (following ExternalProject dependencies, e.g. OpenVDB → Blosc, OpenEXR), and
   writes one `SourceNNN:` line per needed tarball into the spec
   (`<url>#/dep__<Dir>__<file>`).
2. OBS's `download_files` service fetches those URLs.
3. `%prep` copies each into `deps-dl/<Dir>/<file>`, where ExternalProject looks;
   it verifies **upstream's own SHA256** and skips the download.
4. The wxWidgets fork, which upstream clones unpinned from `master`, is
   replaced by a tarball of a pinned commit (`%wx_commit`, the fork's `master`
   at the upstream release date).

Guardrail: `gen_deps.py` aborts if a bundled dependency becomes git-cloned or
loses its SHA256, so a bump cannot silently produce a recipe that needs network.

### Unbundling a library

When a distribution ships a compatible version of a bundled library, switch it
in the spec (set its `DEP_BUILD_*=OFF` and/or drop it from `%deps_targets`, add
the system `BuildRequires`) and re-run `tools/gen_deps.py`.

## Repository layout

```
packages/bambustudio/
  _service                   # OBS: recipe from this repo (obs_scm) + download_files
  _constraints               # disk/memory for the bundled deps + the static link
  bambustudio.spec           # bundled Source list generated by tools/gen_deps.py
  bambustudio.changes
  bambustudio-rpmlintrc
project/
  _meta.xml                  # repository/arch matrix   (osc meta prj -F)
  _config                    # prjconf                  (osc meta prjconf -F)
  bambustudio.meta.xml       # package meta
tools/
  gen_deps.py                # regenerate the bundled Source list from an upstream tree
  bump.py                    # upstream release tracker (run daily by CI)
.github/workflows/upstream-bump.yml
```

## Maintainer workflow

### One-time OBS setup

```sh
P=home:ciriarte:bambustudio
osc meta prj     $P -F project/_meta.xml
osc meta prjconf $P -F project/_config
osc meta pkg $P bambustudio -F project/bambustudio.meta.xml

# The OBS package holds only _service + _constraints; the service pulls the
# recipe from this repo (main) and the tarballs from upstream.
osc co $P bambustudio && cp packages/bambustudio/{_service,_constraints} $P/bambustudio/
(cd $P/bambustudio && osc addremove && osc commit -m "Source the recipe from GitHub")
```

### After changing a recipe

Push to `main`, then re-run the service:

```sh
osc service remoterun home:ciriarte:bambustudio bambustudio
```

(or run the *upstream bump* workflow manually with `runservice` ticked).

### Bumping upstream

Automatic: `.github/workflows/upstream-bump.yml` runs daily. When upstream
publishes a newer stable release it runs `tools/bump.py` (regenerate deps
sources → pin wxWidgets → bump spec and `.changes`), pushes to `main` and
fires the OBS runservice token.

Manual: `tools/bump.py [--version 02.08.02.61]`, review, commit, push, then
re-run the service as above. `tools/bump.py --dry-run` only reports.

Token setup (no OBS password lives in GitHub):

```sh
osc token --create --operation runservice home:ciriarte:bambustudio
gh secret set OBS_SERVICE_TOKEN     # paste the token string
```

If `gen_deps.py`'s guardrail trips on a new release, the run fails (GitHub
emails you); adapt the spec to the new upstream dependency and re-run.

### Local test build

```sh
osc co home:ciriarte:bambustudio bambustudio && cd home:ciriarte:bambustudio/bambustudio
osc service manualrun        # or: osc service runall
osc build openSUSE_Slowroll x86_64
```

Expect ~25 GB of disk and a few hours (bundled deps + the slicer).
