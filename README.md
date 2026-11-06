# Bambu Studio packages for openSUSE

[![upstream bump](https://github.com/ciroiriarte/obs-bambustudio/actions/workflows/upstream-bump.yml/badge.svg)](https://github.com/ciroiriarte/obs-bambustudio/actions/workflows/upstream-bump.yml)

Unofficial native packages of [Bambu Studio](https://github.com/bambulab/BambuStudio),
the 3D printing slicer, built from upstream source on the
[openSUSE Build Service](https://build.opensuse.org/project/show/home:ciriarte:bambustudio).
New upstream releases are packaged automatically.

> Not endorsed or supported by Bambu Lab. Bambu Studio and Bambu Lab are
> trademarks of their owner. Bambu Studio and this packaging are AGPL-3.0.

## Install

```sh
CHANNEL=stable              # or: beta
REPO=openSUSE_Slowroll      # or: openSUSE_Tumbleweed, openSUSE_Leap_16.0
BASE="https://download.opensuse.org/repositories/home:/ciriarte:/bambustudio:/$CHANNEL/$REPO"
sudo zypper addrepo -f "$BASE/home:ciriarte:bambustudio:$CHANNEL.repo"
sudo zypper --gpg-auto-import-keys refresh
sudo zypper install bambustudio
```

Start it from the desktop menu or with `bambu-studio`.

### Channels

| Channel | Follows |
|---------|---------|
| `stable` | the newest stable upstream release |
| `beta` | the newest upstream release including Public Betas, so it is never behind stable |

Add **one** channel only: both ship a package named `bambustudio`. To switch,
remove the current repository (`sudo zypper removerepo home_ciriarte_bambustudio_stable`,
or `_beta`), add the other one, and run `sudo zypper dup --from <new repo alias>`.

### Distributions

| Distribution | `REPO` | Status |
|--------------|--------|--------|
| openSUSE Slowroll | `openSUSE_Slowroll` | available |
| openSUSE Tumbleweed | `openSUSE_Tumbleweed` | available |
| openSUSE Leap 16.0 | `openSUSE_Leap_16.0` | available |
| Rocky Linux 9/10, Ubuntu 24.04, Debian 13 | — | planned |

x86_64 only.

## Troubleshooting

**Camera live view does not decode.** openSUSE's FFmpeg leaves out patented
codecs such as H.264. Install `libavcodec61` and `gstreamer-plugins-libav`
from [Packman](https://en.opensuse.org/Additional_package_repositories#Packman).
Slicing and printing work without them.

**Printers or cloud features.** These need Bambu Lab's closed network plugin,
which Bambu Studio offers to download on first use. It is not part of this
package. The package points the plugin at the system CA certificates
(`SSL_CERT_FILE`) unless you set that variable yourself.

**Crashes.** Install the debug packages so backtraces show source files and lines:

```sh
sudo zypper install bambustudio-debuginfo bambustudio-debugsource
coredumpctl list bambu-studio     # find the crash's PID
coredumpctl info <PID>            # the first stack trace is the crashing thread
```

- Only `libbambu_networking.so` or `libBambuSource.so` frames: a bug in Bambu Lab's
  closed plugin. Report it [upstream](https://github.com/bambulab/BambuStudio/issues).
  A crash while quitting is the known
  [#12200](https://github.com/bambulab/BambuStudio/issues/12200); nothing is lost.
- `bambu-studio` frames on top: [open an issue here](https://github.com/ciroiriarte/obs-bambustudio/issues)
  with the output of `coredumpctl info`.

Bambu Studio's own logs in `~/.config/BambuStudio/log/` are encrypted; only Bambu Lab can read them.

## How it is built

Libraries come from the distribution wherever possible. The few it cannot
provide (Bambu's wxWidgets fork, Boost, OCCT, CGAL, OpenVDB, TBB and a few
others) are built from upstream's own recipes and linked in privately, so
nothing conflicts with system packages.

Build details and the maintainer workflow: [docs/MAINTAINING.md](docs/MAINTAINING.md).
