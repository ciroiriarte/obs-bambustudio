#!/usr/bin/env python3
"""Vendor the npm packages of BambuStudio's device-page web frontend.

Upstream builds src/slic3r/GUI/DeviceWeb/device_page (TypeScript + Vite) during
the CMake build: it downloads Node.js and pnpm, then `pnpm install` pulls ~the
whole lockfile from the npm registry. OBS build workers have no network, so:

  * Node.js comes from the distribution (BuildRequires: nodejs >= 22).
  * pnpm comes from its npm tarball (plain JavaScript, run with the distro
    node), at upstream's PNPM_VERSION -> spec %pnpm_version / Source3.
  * The npm packages come from a pnpm content-addressable store built here with
    `pnpm fetch` against upstream's pnpm-lock.yaml, published as a GitHub
    release asset of this repository -> spec %web_store / Source4.

The store is keyed by the first 12 hex digits of the lockfile's SHA256, so
versions and channels with the same lockfile share one asset, and an asset is
built and uploaded only once. It includes the native optional packages
(esbuild, rollup, ...) for linux x64 and arm64.

Usage: tools/vendor_web.py <upstream-source-dir> --spec PATH [--no-upload]
Requires node, curl, tar with zstd, and gh (authenticated) for the upload.
"""
import argparse
import hashlib
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

REPO = "ciroiriarte/obs-bambustudio"
DEVICE_PAGE = "src/slic3r/GUI/DeviceWeb/device_page"
DEVICE_CMAKE = "src/slic3r/GUI/DeviceWeb/CMakeLists.txt"
SUPPORTED_ARCH = """supportedArchitectures:
  os: [linux]
  cpu: [x64, arm64]
  libc: [glibc]
"""


def set_global(text, name, value):
    new, n = re.subn(rf"^(%global\s+{name}\s+)\S+", rf"\g<1>{value}", text, flags=re.M)
    if n != 1:
        sys.exit(f"spec lacks '%global {name}'")
    return new


def release_exists(tag):
    return subprocess.run(["gh", "release", "view", tag, "-R", REPO],
                          capture_output=True).returncode == 0


def build_store(src, pnpm_version, out):
    with tempfile.TemporaryDirectory(prefix="bbs-web-") as tmp:
        tmp = pathlib.Path(tmp)
        subprocess.run(["curl", "-fsSL", "--retry", "3", "-o", str(tmp / "pnpm.tgz"),
                        f"https://registry.npmjs.org/pnpm/-/pnpm-{pnpm_version}.tgz"], check=True)
        subprocess.run(["tar", "-C", str(tmp), "-xzf", str(tmp / "pnpm.tgz")], check=True)
        work = tmp / "device_page"
        work.mkdir()
        for f in ("package.json", "pnpm-lock.yaml"):
            shutil.copy2(src / DEVICE_PAGE / f, work / f)
        (work / "pnpm-workspace.yaml").write_text(SUPPORTED_ARCH)
        store = tmp / "pnpm-store"
        subprocess.run(["node", str(tmp / "package/bin/pnpm.cjs"), "fetch",
                        "--store-dir", str(store)],
                       cwd=work, check=True,
                       env={"PATH": "/usr/bin:/bin", "HOME": str(tmp),
                            "npm_config_update_notifier": "false"})
        subprocess.run(["tar", "--zstd", "--sort=name", "--owner=0", "--group=0",
                        "--numeric-owner", "-C", str(tmp), "-cf", str(out), "pnpm-store"],
                       check=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("source", type=pathlib.Path, help="extracted upstream BambuStudio tree")
    ap.add_argument("--spec", type=pathlib.Path, required=True)
    ap.add_argument("--no-upload", action="store_true", help="only update the spec")
    args = ap.parse_args()

    cmake = (args.source / DEVICE_CMAKE).read_text()
    m = re.search(r'set\(PNPM_VERSION "([^"]+)"\)', cmake)
    if not m:
        sys.exit(f"no PNPM_VERSION in {DEVICE_CMAKE}; upstream changed the web build")
    pnpm_version = m.group(1)
    lock = (args.source / DEVICE_PAGE / "pnpm-lock.yaml").read_bytes()
    store_id = hashlib.sha256(lock).hexdigest()[:12]
    tag = f"web-store-{store_id}"
    asset = f"device-page-store-{store_id}.tar.zst"

    if args.no_upload:
        print(f"skipping upload check for {tag}")
    elif release_exists(tag):
        print(f"{tag} already published")
    else:
        with tempfile.TemporaryDirectory(prefix="bbs-webout-") as out:
            out = pathlib.Path(out) / asset
            build_store(args.source, pnpm_version, out)
            subprocess.run(["gh", "release", "create", tag, str(out), "-R", REPO,
                            "--title", f"device_page npm store {store_id}", "--latest=false",
                            "--notes", f"pnpm {pnpm_version} store for upstream device_page "
                                       f"pnpm-lock.yaml sha256 {hashlib.sha256(lock).hexdigest()}. "
                                       "Build input for the OBS packages; not an end-user download."],
                           check=True)
            print(f"published {tag} ({out.stat().st_size // 2**20} MiB)")

    text = set_global(args.spec.read_text(), "pnpm_version", pnpm_version)
    args.spec.write_text(set_global(text, "web_store", store_id))
    print(f"{args.spec}: pnpm {pnpm_version}, web store {store_id}")


if __name__ == "__main__":
    main()
