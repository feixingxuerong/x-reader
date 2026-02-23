#!/usr/bin/env python3
"""Backward-compatible wrapper for X-Reader CLI.

This keeps existing usage working:
    python3 fetch.py --url <url>
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from x_reader.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
