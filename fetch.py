#!/usr/bin/env python3
"""兼容入口：保留 python3 fetch.py 的使用方式。

核心实现迁移到 src/x_reader。
"""

from x_reader.service import XReader  # noqa: F401
from x_reader.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
