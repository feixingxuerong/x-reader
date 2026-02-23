#!/usr/bin/env python3
"""Backward-compatible wrapper for Discord bot launcher."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from x_reader.discord_bot import run_bot


if __name__ == "__main__":
    raise SystemExit(run_bot())
