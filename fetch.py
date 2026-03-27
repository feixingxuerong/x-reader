#!/usr/bin/env python3
"""兼容入口：保留 python3 fetch.py 的使用方式。

核心实现位于 src/x_reader。

兼容承诺：支持历史用法 `from fetch import XReader`。
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from x_reader.reader import XReader  # noqa: F401
from x_reader.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
