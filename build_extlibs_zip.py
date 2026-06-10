# -*- coding: utf-8 -*-
"""Build an extlibs zip tagged for the running Python + platform.

Two modes:

  # Full build (recommended) — run with the TARGET QGIS Python:
  python build_extlibs_zip.py
      pip-installs requirements.txt into a temp dir, strips QGIS-provided
      packages (numpy/pandas/scipy/...), and writes extlibs-<tag>.zip
      (e.g. extlibs-cp312-win_amd64.zip) to the plugin root.

  # Manual mode — zip an existing pip --target dir:
  python build_extlibs_zip.py <build_dir> <out_zip>

Commit + push the resulting extlibs-<tag>.zip so the runtime downloader
(extlibs_manager) can fetch the build matching each QGIS Python. The GitHub
Actions workflow (.github/workflows/build-extlibs.yml) builds the full matrix.

Each zip also carries the native ``aria2c`` daemon under ``extlibs/bin/`` — the
Landsat batch download spawns it via agrigee_lite's downloader and aria2 is not
a pip package. On Windows the official static build is downloaded; on
Linux/macOS the runner's system aria2c (installed by the workflow) is copied.
"""
import os
import shutil
import subprocess
import sys
import sysconfig
import tempfile
import urllib.request
import zipfile

_HERE = os.path.dirname(os.path.abspath(__file__))
_REQUIREMENTS = os.path.join(_HERE, "requirements.txt")

# Official aria2 static Windows build. Bump the version here to update the
# bundled daemon; the asset is a zip containing ``.../aria2c.exe``.
_ARIA2_WIN_URL = (
    "https://github.com/aria2/aria2/releases/download/"
    "release-1.37.0/aria2-1.37.0-win-64bit-build1.zip"
)

# Keep in sync with extlibs_manager._QGIS_PROVIDED.
_QGIS_PROVIDED = (
    "numpy", "pandas", "scipy", "matplotlib", "requests", "certifi",
    "urllib3", "idna", "charset_normalizer", "plotly",
)


def current_tag() -> str:
    plat = sysconfig.get_platform().replace("-", "_").replace(".", "_")
    return f"cp{sys.version_info.major}{sys.version_info.minor}-{plat}"


def zip_dir(src, out):
    zf = zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9)
    n = 0
    for root, _, files in os.walk(src):
        for f in files:
            fp = os.path.join(root, f)
            rel = os.path.relpath(fp, src).replace(os.sep, "/")
            zf.write(fp, "extlibs/" + rel)
            n += 1
    zf.close()
    print("files", n, "zip MB", round(os.path.getsize(out) / 1e6, 1))


def _strip(target):
    # remove QGIS-provided packages + junk to shrink the zip
    for entry in list(os.listdir(target)):
        low = entry.lower()
        full = os.path.join(target, entry)
        drop = any(low == p or low.startswith(p + "-") or low.startswith(p + ".")
                   for p in _QGIS_PROVIDED)
        if drop:
            shutil.rmtree(full, ignore_errors=True) if os.path.isdir(full) else os.remove(full)
    for root, dirs, files in os.walk(target):
        for d in list(dirs):
            if d in ("__pycache__", "tests", "test"):
                shutil.rmtree(os.path.join(root, d), ignore_errors=True)
        for f in files:
            if f.endswith((".whl", ".pyc")):
                try:
                    os.remove(os.path.join(root, f))
                except OSError:
                    pass


def bundle_aria2c(build):
    """Place the native aria2c binary at ``<build>/bin/`` so the zip ships it as
    ``extlibs/bin/aria2c[.exe]``. Best-effort: on a platform where no binary can
    be obtained the directory is left out, and the plugin's runtime PATH lookup
    (or a clear error) covers the batch download."""
    bin_dir = os.path.join(build, "bin")
    os.makedirs(bin_dir, exist_ok=True)

    if sys.platform.startswith("win"):
        dest = os.path.join(bin_dir, "aria2c.exe")
        tmp_zip = os.path.join(build, "_aria2_win.zip")
        try:
            print(f"download aria2c <- {_ARIA2_WIN_URL}")
            urllib.request.urlretrieve(_ARIA2_WIN_URL, tmp_zip)  # noqa: S310
            with zipfile.ZipFile(tmp_zip) as zf:
                member = next(n for n in zf.namelist() if n.endswith("aria2c.exe"))
                with zf.open(member) as src, open(dest, "wb") as out:
                    shutil.copyfileobj(src, out)
            print("bundled aria2c.exe")
            return
        except Exception as e:
            print(f"WARNING: could not bundle aria2c.exe: {e}")
    else:
        # Linux/macOS: copy the runner's system aria2c (the workflow installs it
        # via apt/brew). These are dynamically linked, so this is best-effort.
        src = shutil.which("aria2c")
        if src:
            dest = os.path.join(bin_dir, "aria2c")
            shutil.copy2(src, dest)
            os.chmod(dest, 0o755)
            print(f"bundled aria2c from {src}")
            return
        print("aria2c not found on PATH; not bundling (runtime PATH fallback)")

    # Nothing bundled — drop the empty dir so it doesn't clutter the zip.
    try:
        os.rmdir(bin_dir)
    except OSError:
        pass


def full_build():
    tag = current_tag()
    # Write to the plugin root (committed + served by the raw GitHub URL that
    # extlibs_manager fetches).
    out = os.path.join(_HERE, f"extlibs-{tag}.zip")
    build = tempfile.mkdtemp(prefix="ravi_extlibs_")
    try:
        print(f"pip install -> {build}")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--target", build,
             "-r", _REQUIREMENTS, "--no-warn-script-location"],
            check=True,
        )
        _strip(build)
        bundle_aria2c(build)
        zip_dir(build, out)
        print(f"Done: extlibs-{tag}.zip")
    finally:
        shutil.rmtree(build, ignore_errors=True)


def main():
    if len(sys.argv) == 3:
        zip_dir(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 1:
        full_build()
    else:
        sys.exit("usage: build_extlibs_zip.py [<build_dir> <out_zip>]")


if __name__ == "__main__":
    main()
