"""Hatchling build hook that downloads the prebuilt tectonic binary for a
given target platform and packages it as a platform-specific wheel.

The target platform is selected via the TECTO_TARGET environment variable,
which must be one of the keys in PLATFORMS. CI sets this via a matrix so
each job produces a single platform-tagged wheel.
"""
from __future__ import annotations

import os
import shutil
import tarfile
import tempfile
import urllib.request
import zipfile
from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


# wheel platform tag -> (upstream rust triple, archive extension)
PLATFORMS: dict[str, tuple[str, str]] = {
    "macosx_11_0_arm64":     ("aarch64-apple-darwin",       "tar.gz"),
    "macosx_10_12_x86_64":   ("x86_64-apple-darwin",        "tar.gz"),
    "manylinux2014_x86_64":  ("x86_64-unknown-linux-gnu",   "tar.gz"),
    "musllinux_1_2_x86_64":  ("x86_64-unknown-linux-musl",  "tar.gz"),
    "musllinux_1_2_aarch64": ("aarch64-unknown-linux-musl", "tar.gz"),
    "win_amd64":             ("x86_64-pc-windows-msvc",     "zip"),
}


class CustomBuildHook(BuildHookInterface):
    PLUGIN_NAME = "custom"

    def initialize(self, version: str, build_data: dict) -> None:
        target = os.environ.get("TECTO_TARGET")
        if not target:
            raise RuntimeError(
                "TECTO_TARGET must be set to one of: " + ", ".join(PLATFORMS)
            )
        if target not in PLATFORMS:
            raise RuntimeError(f"unknown TECTO_TARGET={target!r}")

        triple, ext = PLATFORMS[target]
        upstream_version = self.metadata.version
        is_windows = target == "win_amd64"
        # Upstream binary name inside the release archive.
        archive_bin = "tectonic.exe" if is_windows else "tectonic"
        exe_suffix = ".exe" if is_windows else ""
        # We install the binary twice, under two names:
        #   - `tecto`    — matches package name so `uvx tecto` works
        #   - `tectonic` — matches upstream name so existing scripts/docs work
        installed_names = [f"tecto{exe_suffix}", f"tectonic{exe_suffix}"]

        url = (
            "https://github.com/tectonic-typesetting/tectonic/releases/download/"
            f"tectonic%40{upstream_version}/"
            f"tectonic-{upstream_version}-{triple}.{ext}"
        )

        staging = Path(self.root) / "build" / "staging" / target
        if staging.exists():
            shutil.rmtree(staging)
        staging.mkdir(parents=True)

        self.app.display_info(f"[tecto] downloading {url}")
        with tempfile.NamedTemporaryFile(suffix=f".{ext}", delete=False) as tmp:
            urllib.request.urlretrieve(url, tmp.name)
            archive_path = tmp.name

        # Extract once, then copy into a distinct path for each installed name.
        # shared_scripts is source->dest; giving each its own source file
        # ensures pip sees two independent scripts, and each lands in bin/.
        shared_scripts = {}
        try:
            first: Path | None = None
            for name in installed_names:
                dest = staging / name
                if first is None:
                    _extract_binary(archive_path, ext, archive_bin, dest)
                    first = dest
                else:
                    shutil.copyfile(first, dest)
                if not is_windows:
                    dest.chmod(0o755)
                shared_scripts[str(dest)] = name
        finally:
            os.unlink(archive_path)

        build_data["shared_scripts"] = shared_scripts
        build_data["tag"] = f"py3-none-{target}"
        build_data["pure_python"] = False
        build_data["infer_tag"] = False


def _extract_binary(archive: str, ext: str, bin_name: str, dest: Path) -> None:
    if ext == "tar.gz":
        with tarfile.open(archive) as tf:
            for member in tf.getmembers():
                if Path(member.name).name == bin_name:
                    src = tf.extractfile(member)
                    if src is None:
                        continue
                    with open(dest, "wb") as out:
                        shutil.copyfileobj(src, out)
                    return
    else:
        with zipfile.ZipFile(archive) as zf:
            for name in zf.namelist():
                if Path(name).name == bin_name:
                    with zf.open(name) as src, open(dest, "wb") as out:
                        shutil.copyfileobj(src, out)
                    return
    raise RuntimeError(f"{bin_name} not found in {archive}")
