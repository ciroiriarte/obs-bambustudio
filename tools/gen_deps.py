#!/usr/bin/env python3
"""Regenerate the dependency Source list of bambustudio-deps.spec.

OBS build workers have no network, but BambuStudio's deps superbuild
(deps/CMakeLists.txt) downloads ~23 tarballs at build time through CMake
ExternalProject. This script configures that superbuild (configure only,
nothing is built or downloaded) with the same flags the spec uses, reads the
download scripts ExternalProject generates, and rewrites the block between the
BEGIN/END markers in the spec with one SourceNNN line per tarball:

    Source100: <upstream url>#/dep__<Dir>__<file>

download_files (OBS source service) fetches each URL and stores it under the
name after "#/". %prep copies it to deps-dl/<Dir>/<file>, the exact path
ExternalProject looks at; it finds the file, verifies upstream's SHA256 and
skips the download.

Guardrail: the only git-based dependency allowed on Linux is the bambulab
wxWidgets fork (packaged as Source1 at a pinned commit). Any other git clone,
or a download without a SHA256, aborts so a bump cannot silently produce a
recipe that needs network at build time.

Usage: tools/gen_deps.py <upstream-source-dir> [--spec PATH]
"""
import argparse
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SPEC = ROOT / "packages/bambustudio-deps/bambustudio-deps.spec"
BEGIN = "# BEGIN generated deps sources (tools/gen_deps.py)"
END = "# END generated deps sources"
FIRST_SOURCE = 100


def spec_flags(spec_text):
    m = re.search(r"^%global\s+deps_cmake_flags\s+(.+)$", spec_text, re.M)
    if not m:
        sys.exit("spec has no '%global deps_cmake_flags' line")
    return m.group(1).split()


def parse_download_script(path, dl_dir):
    text = path.read_text()
    files = set(re.findall(r"file='([^']+)'", text))
    if len(files) != 1:
        sys.exit(f"{path.name}: expected one target file, found {files}")
    rel = pathlib.PurePosixPath(files.pop()).relative_to(dl_dir)
    if len(rel.parts) != 2:
        sys.exit(f"{path.name}: unexpected download path {rel}")
    sha = re.search(r'STREQUAL "([0-9a-fA-F]{64})"', text)
    if not sha:
        sys.exit(f"{path.name}: no SHA256 in the upstream recipe; refusing an unverified source")
    urls = re.findall(r"\[====\[(\S+?)\]====\]", text)
    if not urls:
        sys.exit(f"{path.name}: no URL found")
    # Prefer https when upstream lists mirrors (MPFR lists an http mirror first).
    url = next((u for u in urls if u.startswith("https://")), urls[0])
    return rel.parts[0], rel.parts[1], url, sha.group(1).lower()


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("source", type=pathlib.Path, help="extracted upstream BambuStudio tree")
    ap.add_argument("--spec", type=pathlib.Path, default=SPEC)
    args = ap.parse_args()

    spec_text = args.spec.read_text()
    with tempfile.TemporaryDirectory(prefix="bbs-depcfg-") as tmp:
        tmp = pathlib.Path(tmp)
        dl_dir = tmp / "dl"
        subprocess.run(
            ["cmake", "-Wno-dev", "-S", str(args.source / "deps"), "-B", str(tmp / "build"),
             f"-DDEP_DOWNLOAD_DIR={dl_dir}", *spec_flags(spec_text)],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        gitclones = sorted(p.name for p in (tmp / "build").rglob("*-gitclone.cmake"))
        if gitclones != ["dep_wxWidgets-gitclone.cmake"]:
            sys.exit(f"git-based deps changed upstream: {gitclones}; "
                     "only the wxWidgets fork is handled (Source1)")

        entries = sorted(parse_download_script(p, dl_dir)
                         for p in (tmp / "build").rglob("download-dep_*.cmake"))

    lines = [BEGIN]
    for i, (d, f, url, sha) in enumerate(entries, FIRST_SOURCE):
        lines.append(f"# sha256 {sha}")
        lines.append(f"Source{i}:{' ' * max(1, 6 - len(str(i)))}{url}#/dep__{d}__{f}")
    lines.append(END)

    pat = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END), re.S)
    if not pat.search(spec_text):
        sys.exit("spec lacks the generated-sources markers")
    args.spec.write_text(pat.sub("\n".join(lines), spec_text))
    print(f"{len(entries)} dependency sources written to {args.spec}")


if __name__ == "__main__":
    main()
