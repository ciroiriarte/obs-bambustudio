# obs-bambustudio — Bambu Studio packages for Linux distributions

[![upstream bump](https://github.com/ciroiriarte/obs-bambustudio/actions/workflows/upstream-bump.yml/badge.svg)](https://github.com/ciroiriarte/obs-bambustudio/actions/workflows/upstream-bump.yml)

Community/**unofficial** native packages of [Bambu Studio](https://github.com/bambulab/BambuStudio),
the 3D printing slicer, built **from upstream source** on the
[openSUSE Build Service](https://build.opensuse.org/project/show/home:ciriarte:bambustudio),
in two channels. New upstream releases are picked up and rebuilt automatically.

> Bambu Studio and Bambu Lab are trademarks of their owner. This project is
> community-maintained and **not endorsed or supported by Bambu Lab**.
> Bambu Studio is licensed AGPL-3.0; so is this packaging.

- **Upstream:** https://github.com/bambulab/BambuStudio

## Channels

| Channel | OBS project | Tracks |
|---------|-------------|--------|
| **stable** | `home:ciriarte:bambustudio:stable` | newest upstream release *not* marked pre-release |
| **beta** | `home:ciriarte:bambustudio:beta` | newest upstream release of any kind ("Public Beta" or stable), so it is never behind stable |

`home:ciriarte:bambustudio` itself is only the parent; it holds no packages.
Both channels ship a package named `bambustudio` — add **one** channel's
repository, not both.

## Supported targets

| Distro | `REPO` token | Arch | Status |
|--------|--------------|------|--------|
| openSUSE Slowroll | `openSUSE_Slowroll` | x86_64 | building (stable and beta) |
| openSUSE Tumbleweed / Leap 16.0 | — | — | planned |
| Rocky Linux 9 / 10 | — | — | planned |
| Ubuntu 24.04 / Debian 13 | — | — | planned (needs `debian.*` recipe) |

OBS publishes Slowroll for x86_64 only.

## Install

### openSUSE (zypper)

```sh
CHANNEL=stable              # or: beta
REPO=openSUSE_Slowroll
BASE="https://download.opensuse.org/repositories/home:/ciriarte:/bambustudio:/$CHANNEL/$REPO"
sudo zypper addrepo -f "$BASE/home:ciriarte:bambustudio:$CHANNEL.repo"
sudo zypper --gpg-auto-import-keys refresh
sudo zypper install bambustudio
```

To switch channel, remove the other repository first
(`sudo zypper removerepo home_ciriarte_bambustudio_stable`, or `_beta`) and run
`sudo zypper dup --from <new repo alias>` (going beta → stable is a downgrade
until stable catches up).

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
FFmpeg 7, OpenCV, assimp, GLEW, GLFW, NLopt, cereal, libharu, GMP/MPFR,
freetype, libpng/libjpeg/libtiff/expat, zlib.

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

### Adapting upstream to system libraries

Upstream's CMake assumes its own bundled copies. The spec bridges the
differences; each step checks that it applied and fails the build otherwise,
so an upstream change surfaces as a clear `%prep` error on the next bump:

| Where | Adjustment | Why |
|-------|------------|-----|
| `%prep` | `<hpdf/...>` includes → `<...>` | system libharu installs `hpdf*.h` flat in `/usr/include` |
| `%prep` | `cereal` INTERFACE target → `cereal::cereal` | system cereal exports only the namespaced target; the bare name became `-lcereal` |
| `%prep` | `opencv_world` → `${OpenCV_LIBS}` (core, imgproc, imgcodecs) | distro OpenCV is per-module, not the monolithic world library |
| `%prep` | drop the `OSMesa` link | never called directly (GLFW dlopens it); current Mesa no longer ships libOSMesa |
| `%install` | delete `include/mcut`, `/usr/LICENSE.txt`, `/usr/README.md` | the vendored, statically linked mcut installs its dev files into the prefix |
| configure | `-DCMAKE_SKIP_INSTALL_RPATH=ON` | upstream sets `$ORIGIN` RUNPATH on Linux (rpmlint badness 10000) |
| BuildRequires | `libquadmath-devel` | Boost.Multiprecision includes `quadmath.h` when GCC enables `__float128` |

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

5. Some bundled recipes download more at build time themselves (beta's
   OpenMeshCraft fetches Eigen, parallel-hashmap, oneTBB and fmt from a
   generated script). `gen_deps.py` collects those url + SHA256 pairs as
   Sources too (`nested__<Dir>__<file>`), and `%prep` rewrites each URL to a
   `file://` path to its Source (`%nested_fetches`); upstream's hash check
   still applies.

Guardrail: `gen_deps.py` aborts if a bundled dependency becomes git-cloned,
loses its SHA256, or downloads through a mechanism it does not recognize, so a
bump cannot silently produce a recipe that needs network.

### Device page web frontend (Node.js)

Bambu Studio includes a TypeScript/Vite web UI
(`src/slic3r/GUI/DeviceWeb/device_page`) that upstream builds during the CMake
build by downloading Node.js and pnpm and running `pnpm install` against npm.
Offline on OBS instead:

- **Node.js** is the distribution's (`BuildRequires: nodejs >= 22`).
- **pnpm** is its npm tarball (plain JavaScript) at upstream's `PNPM_VERSION`,
  run by the distro `node` (`%pnpm_version`, Source3).
- **npm packages** come from a pnpm store that `tools/vendor_web.py` builds with
  `pnpm fetch` against upstream's `pnpm-lock.yaml` and publishes as a release
  asset of this repo (`web-store-<id>`, Source4). `<id>` is the first 12 hex
  digits of the lockfile's SHA256, so channels/versions with the same lockfile
  share one asset. It includes native optional packages for linux x64 and arm64.

`%prep` seeds the `node-cache` directory upstream's CMake checks with the distro
`node` and an offline `pnpm` wrapper (`install --offline --frozen-lockfile`
from the vendored store), so nothing is downloaded and the frontend is still
built from source on OBS.

### Unbundling a library

When a distribution ships a compatible version of a bundled library, switch it
in the spec (set its `DEP_BUILD_*=OFF` and/or drop it from `%deps_targets`, add
the system `BuildRequires`) and re-run `tools/gen_deps.py`.

## Repository layout

```
packages/<channel>/bambustudio/     # channel = stable | beta
  _service                   # OBS: recipe from this repo (obs_scm) + download_files
  _constraints               # disk/memory for the bundled deps + the static link
  bambustudio.spec           # bundled Source list generated by tools/gen_deps.py
  bambustudio.changes
  bambustudio-rpmlintrc
project/
  _meta.xml                  # parent project home:ciriarte:bambustudio (no repos)
  <channel>/_meta.xml        # repository/arch matrix   (osc meta prj -F)
  <channel>/_config          # prjconf                  (osc meta prjconf -F)
  <channel>/bambustudio.meta.xml   # package meta
tools/
  gen_deps.py                # regenerate the bundled Source list from an upstream tree
  vendor_web.py              # build + publish the device_page npm store, set %web_store
  bump.py                    # upstream release tracker per channel (run daily by CI)
.github/workflows/upstream-bump.yml
```

## Maintainer workflow

### One-time OBS setup

```sh
osc meta prj home:ciriarte:bambustudio -F project/_meta.xml     # parent
for ch in stable beta; do
  P=home:ciriarte:bambustudio:$ch
  osc meta prj     $P -F project/$ch/_meta.xml
  osc meta prjconf $P -F project/$ch/_config
  osc meta pkg $P bambustudio -F project/$ch/bambustudio.meta.xml
  # The OBS package holds only _service + _constraints; the service pulls the
  # channel's recipe from this repo (main) and the tarballs from upstream.
  osc co $P bambustudio && cp packages/$ch/bambustudio/{_service,_constraints} $P/bambustudio/
  (cd $P/bambustudio && osc addremove && osc commit -m "Source the recipe from GitHub")
done
```

### After changing a recipe

Push to `main`, then re-run the service:

```sh
osc service remoterun home:ciriarte:bambustudio:stable bambustudio   # and/or :beta
```

(or run the *upstream bump* workflow manually with `runservice` ticked).

### Bumping upstream

Automatic: `.github/workflows/upstream-bump.yml` runs daily and processes both
channels in turn. When a channel's pick (see *Channels*) is newer than its
packaged version it runs `tools/bump.py --channel <ch>` (regenerate bundled
sources → publish the npm store if the lockfile changed → pin wxWidgets →
bump spec and `.changes`), pushes to `main` and fires
the OBS runservice token for that channel.

Manual: `tools/bump.py --channel stable|beta [--version 02.08.02.61]`, review,
commit, push, then re-run the service as above. `--dry-run` only reports.

A recipe fix needed by a new upstream version usually lands in `beta` first.
When stable reaches that version, carry the fix over to
`packages/stable/bambustudio/bambustudio.spec` (keep the stable `Version`,
`%upstream_ver`, `%wx_commit` and generated Source block).

Token setup (no OBS password lives in GitHub):

```sh
osc token --create --operation runservice   # no project/package binding: serves both channels
gh secret set OBS_SERVICE_TOKEN -R ciroiriarte/obs-bambustudio   # paste the token string
```

If `gen_deps.py`'s guardrail trips on a new release, the run fails (GitHub
emails you); adapt the spec to the new upstream dependency and re-run.

### Local test build

```sh
osc co home:ciriarte:bambustudio:stable bambustudio && cd home:ciriarte:bambustudio:stable/bambustudio
osc service manualrun        # or: osc service runall
osc build openSUSE_Slowroll x86_64
```

Expect ~25 GB of disk and a few hours (bundled deps + the slicer).
