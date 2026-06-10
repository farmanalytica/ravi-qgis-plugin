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
"""
import os
import shutil
import subprocess
import sys
import sysconfig
import tempfile
import zipfile

_HERE = os.path.dirname(os.path.abspath(__file__))
_REQUIREMENTS = os.path.join(_HERE, "requirements.txt")

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
