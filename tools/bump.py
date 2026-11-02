#!/usr/bin/env python3
"""Track upstream BambuStudio stable releases and bump the recipe.

Detects the newest *stable* GitHub release of bambulab/BambuStudio (pre-release
"Public Beta" builds are skipped). If it is newer than the packaged version:

  1. fetches the release tarball and extracts deps/ + cmake/ only,
  2. regenerates the bundled-dependency Source list (tools/gen_deps.py),
  3. pins the bambulab/wxWidgets fork to the last master commit at or before
     the release date (upstream consumes "GIT_TAG master", unpinned),
  4. updates Version / upstream_ver / wx_commit in the spec and prepends a
     .changes entry.

Usage: tools/bump.py [--dry-run] [--version 02.08.02.61]
  --dry-run   print "would bump A -> B" (or "up to date") and change nothing
  --version   bump to this upstream tag (without the leading v) instead of latest
"""
import argparse
import datetime
import json
import os
import pathlib
import re
import subprocess
import sys
import tarfile
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
PKGS = ROOT / "packages"
SPEC = PKGS / "bambustudio" / "bambustudio.spec"
UPSTREAM = "bambulab/BambuStudio"
WX_FORK = "bambulab/wxWidgets"
PACKAGER = "Ciro Iriarte <ciro.iriarte+software@gmail.com>"
CACHE = ROOT / ".cache"


def gh(path):
    req = urllib.request.Request(f"https://api.github.com/{path}",
                                 headers={"Accept": "application/vnd.github+json"})
    if os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", f"Bearer {os.environ['GITHUB_TOKEN']}")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def rpm_version(upstream_ver):
    """02.08.02.61 -> 2.8.2.61"""
    return ".".join(str(int(x)) for x in upstream_ver.split("."))


def key(upstream_ver):
    return tuple(int(x) for x in upstream_ver.split("."))


def current_upstream_ver():
    m = re.search(r"^%global\s+upstream_ver\s+(\S+)", SPEC.read_text(), re.M)
    return m.group(1)


def set_global(text, name, value):
    new, n = re.subn(rf"^(%global\s+{name}\s+)\S+", rf"\g<1>{value}", text, flags=re.M)
    if n != 1:
        sys.exit(f"could not set %global {name}")
    return new


def set_version(text, version):
    new, n = re.subn(r"^(Version:\s+)\S+", rf"\g<1>{version}", text, flags=re.M)
    if n != 1:
        sys.exit("could not set Version:")
    return new


def prepend_changes(pkg, lines):
    path = PKGS / pkg / f"{pkg}.changes"
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%a %b %e %H:%M:%S UTC %Y")
    entry = "-" * 67 + f"\n{stamp} - {PACKAGER}\n\n" + "\n".join(lines) + "\n\n"
    path.write_text(entry + path.read_text())


def fetch_source(upstream_ver):
    """Download the release tarball and extract only what gen_deps needs."""
    CACHE.mkdir(exist_ok=True)
    tarball = CACHE / f"BambuStudio-{upstream_ver}.tar.gz"
    if not tarball.exists():
        url = f"https://github.com/{UPSTREAM}/archive/refs/tags/v{upstream_ver}.tar.gz"
        subprocess.run(["curl", "-fsSL", "--retry", "3", "-o", str(tarball), url], check=True)
    top = f"BambuStudio-{upstream_ver}"
    dest = CACHE / "src"
    with tarfile.open(tarball) as tf:
        members = [m for m in tf.getmembers()
                   if m.name.startswith((f"{top}/deps/", f"{top}/cmake/"))]
        tf.extractall(dest, members=members, filter="data")
    return dest / top


def wx_commit_at(when):
    commits = gh(f"repos/{WX_FORK}/commits?sha=master&until={when}&per_page=1")
    if not commits:
        sys.exit(f"no {WX_FORK} commit before {when}")
    return commits[0]["sha"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--version", help="upstream version without the leading v")
    args = ap.parse_args()

    if args.version:
        rel = gh(f"repos/{UPSTREAM}/releases/tags/v{args.version}")
    else:
        rel = gh(f"repos/{UPSTREAM}/releases/latest")  # excludes pre-releases
    new = rel["tag_name"].lstrip("v")
    cur = current_upstream_ver()

    if key(new) <= key(cur) and not args.version:
        print(f"up to date: {cur}")
        return
    if args.dry_run:
        print(f"would bump {cur} -> {new}")
        return

    src = fetch_source(new)
    subprocess.run([sys.executable, str(ROOT / "tools/gen_deps.py"), str(src)], check=True)

    wx = wx_commit_at(rel["published_at"])
    version = rpm_version(new)
    text = set_version(set_global(SPEC.read_text(), "upstream_ver", new), version)
    SPEC.write_text(set_global(text, "wx_commit", wx))

    notes = f"https://github.com/{UPSTREAM}/releases/tag/v{new}"
    prepend_changes("bambustudio", [f"- Update to {version} (upstream v{new})",
                                    f"  * Release notes: {notes}",
                                    "  * Regenerate bundled dependency sources from upstream deps/",
                                    f"  * Pin {WX_FORK} at {wx[:12]}"])
    print(f"bumped {cur} -> {new} (wxWidgets {wx[:12]})")


if __name__ == "__main__":
    main()
