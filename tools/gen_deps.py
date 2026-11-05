#!/usr/bin/env python3
"""Regenerate the bundled-dependency Source list of a bambustudio.spec.

Most BambuStudio dependencies come from the target distribution. The few that
cannot (the bambulab wxWidgets fork, Boost, TBB, OCCT, CGAL, OpenVDB, libnoise)
are built from upstream's own superbuild (deps/CMakeLists.txt), which downloads
tarballs at build time through CMake ExternalProject. OBS build workers have no
network, so this script works out which tarballs those builds need and writes
them into the spec as Source lines:

    Source100: <upstream url>#/dep__<Dir>__<file>

How: configure the superbuild (configure only, nothing is built or downloaded)
with the spec's %deps_cmake_flags, ask ninja for a dry run of the spec's
%deps_targets (this follows ExternalProject DEPENDS, e.g. OpenVDB -> Blosc,
OpenEXR), and read the download scripts of exactly those dependencies.

download_files (OBS source service) fetches each URL and stores it under the
name after "#/". %prep copies it to deps-dl/<Dir>/<file>, the exact path
ExternalProject looks at; it verifies upstream's SHA256 and skips the download.

Guardrail: the only git-based dependency allowed is the bambulab wxWidgets fork
(Source1, pinned commit). Any other git clone, or a download without a SHA256,
aborts so a bump cannot produce a recipe that needs network at build time.

Usage: tools/gen_deps.py <upstream-source-dir> --spec packages/<channel>/bambustudio/bambustudio.spec
"""
import argparse
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
BEGIN = "# BEGIN generated deps sources (tools/gen_deps.py)"
END = "# END generated deps sources"
FIRST_SOURCE = 100
GIT_DEPS = {"wxWidgets"}  # handled in the spec (Source1)


def spec_global(spec_text, name):
    m = re.search(rf"^%global\s+{name}\s+(.+)$", spec_text, re.M)
    if not m:
        sys.exit(f"spec has no '%global {name}' line")
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


def nested_downloads(deps_dir, needed):
    """Downloads a bundled recipe performs itself, outside ExternalProject.

    Example: deps/OpenMeshCraft generates a prepare_source.cmake that fetches
    Eigen, parallel-hashmap, oneTBB and fmt with file(DOWNLOAD) at build time.
    Every such call in upstream's recipes passes a quoted https URL followed
    by a quoted SHA256; collect those so the spec can ship them as Sources.
    Any other file(DOWNLOAD)/FetchContent in a needed recipe aborts.
    """
    found = []
    for d in sorted(needed):
        for f in sorted((deps_dir / d).glob("*.cmake")):
            text = f.read_text()
            pairs = re.findall(r'"(https://[^"\s]+)"\s*"([0-9A-Fa-f]{64})"', text)
            calls = len(re.findall(r"^\s*\w+\(\s*$\s*\"https://", text, re.M))
            raw = len(re.findall(r"file\(DOWNLOAD|FetchContent_Declare", text))
            # omc-style helper: one file(DOWNLOAD) inside the helper function,
            # invoked once per (url, sha) pair.
            if raw and not pairs:
                sys.exit(f"{f}: unhandled download mechanism (no url+sha256 pairs)")
            if calls and calls != len(pairs):
                sys.exit(f"{f}: {calls} nested download calls but {len(pairs)} with a SHA256")
            found += [(d, url, sha.lower()) for url, sha in pairs]
    return found


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("source", type=pathlib.Path, help="extracted upstream BambuStudio tree")
    ap.add_argument("--spec", type=pathlib.Path, required=True,
                    help="packages/<channel>/bambustudio/bambustudio.spec")
    args = ap.parse_args()

    spec_text = args.spec.read_text()
    flags = spec_global(spec_text, "deps_cmake_flags")
    targets = spec_global(spec_text, "deps_targets")
    with tempfile.TemporaryDirectory(prefix="bbs-depcfg-") as tmp:
        tmp = pathlib.Path(tmp)
        build, dl_dir = tmp / "build", tmp / "dl"
        subprocess.run(
            ["cmake", "-Wno-dev", "-G", "Ninja", "-S", str(args.source / "deps"), "-B", str(build),
             f"-DDEP_DOWNLOAD_DIR={dl_dir}", *flags],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        dry = subprocess.run(["ninja", "-C", str(build), "-n", *targets],
                             check=True, capture_output=True, text=True).stdout
        needed = set(re.findall(r"Performing download step .*? for 'dep_(\w+)'", dry))
        missing = {t.removeprefix("dep_") for t in targets} - needed
        if missing:
            sys.exit(f"ninja dry run did not schedule a download for {missing}")

        git = {p.name.removeprefix("dep_").removesuffix("-gitclone.cmake")
               for p in build.rglob("*-gitclone.cmake")} & needed
        if git != GIT_DEPS & needed:
            sys.exit(f"git-based deps changed upstream: {sorted(git)}; only {GIT_DEPS} is handled")

        entries = sorted(
            parse_download_script(build / f"dep_{d}-prefix/src/dep_{d}-stamp/download-dep_{d}.cmake", dl_dir)
            for d in needed - GIT_DEPS)

    nested = nested_downloads(args.source / "deps", needed)

    lines = [BEGIN]
    i = FIRST_SOURCE
    for d, f, url, sha in entries:
        lines.append(f"# sha256 {sha}")
        lines.append(f"Source{i}:      {url}#/dep__{d}__{f}")
        i += 1
    fetch_map = []
    for d, url, sha in nested:
        f = f"nested__{d}__{url.rsplit('/', 1)[1]}"
        lines.append(f"# nested download in deps/{d}, sha256 {sha}")
        lines.append(f"Source{i}:      {url}#/{f}")
        fetch_map.append(f"{url}@@{f}")
        i += 1
    # No '%' in generated comments: rpm expands macros there, and openSUSE's
    # %prep macro injects the debuginfo/debugsource subpackages where it expands.
    lines.append("# URL@@file map for the prep section: nested downloads are rewritten to file:// Sources")
    lines.append("%global nested_fetches " + (" ".join(fetch_map) or "%{nil}"))
    lines.append(END)

    pat = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END), re.S)
    if not pat.search(spec_text):
        sys.exit("spec lacks the generated-sources markers")
    args.spec.write_text(pat.sub("\n".join(lines), spec_text))
    print(f"{len(entries)} bundled dependency sources ({', '.join(sorted(needed))}) "
          f"+ {len(nested)} nested downloads written to {args.spec}")


if __name__ == "__main__":
    main()
