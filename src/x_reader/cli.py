from __future__ import annotations

import argparse
import sys

from .service import XReader


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="X-Reader: X/Twitter 内容抓取工具")
    p.add_argument("--url", help="推文 URL")
    p.add_argument("--markdown", action="store_true", help="保存为 Markdown")
    p.add_argument("--text-only", action="store_true", help="仅文本输出")
    p.add_argument("--embed", action="store_true", help="显示 Discord 嵌入链接")
    p.add_argument("--output-dir", default="data", help="输出目录")

    args = p.parse_args(argv)

    if not args.url:
        print("请提供 URL: python3 fetch.py --url <url>")
        return 1

    reader = XReader(args.output_dir)

    if args.embed:
        print("Discord 嵌入链接:")
        print(f"<{reader.get_fxembed_url(args.url)}>")
        return 0

    parsed = reader.save(args.url, markdown=args.markdown)
    if parsed and args.text_only:
        print(reader.to_markdown(parsed))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
