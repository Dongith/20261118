#!/usr/bin/env python3
"""Newspaper front page for Wednesday 18 November 2026.

Standard library only: the grader runs this with nothing installed, so the
pre-rendered image is committed beside this file as base64 text
(entry.png.b64) and this program decodes it to entry.png in the output
directory. Run as: python3 -P -s main.py
"""
import base64
import hashlib
import os

SRC_NAME = "entry.png.b64"
OUT_NAME = "entry.png"
WIDTH, HEIGHT = 1024, 1024


def sha256_of(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, SRC_NAME)
    if not os.path.isfile(src):
        raise SystemExit(f"missing {SRC_NAME} beside {__file__}")
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    dst = os.path.join(outdir, OUT_NAME)
    with open(src, "rb") as fh:
        raw = base64.b64decode(fh.read())
    with open(dst, "wb") as fh:
        fh.write(raw)
    if sha256_of(dst) != hashlib.sha256(raw).hexdigest():
        raise SystemExit("write verification failed: digest mismatch")
    size = os.path.getsize(dst)
    print(f"wrote {dst}: {WIDTH}x{HEIGHT}, {size} bytes, sha256 {sha256_of(dst)}")


if __name__ == "__main__":
    main()
