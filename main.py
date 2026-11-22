#!/usr/bin/env python3
"""Entrypoint: copy the pre-rendered cover to the grader's output dir.

Stdlib only, no network, deterministic: the bytes written are exactly the
bytes of entry.png shipped in this repository.
"""

import os
import shutil
import sys


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
