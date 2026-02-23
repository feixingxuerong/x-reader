"""CLI for X-Reader."""

from __future__ import annotations

import argparse

from .reader import XReader


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="X-Reader: X/Twitter 内容抓取工具")
    parser.add_argument("--url", help="推文 URL")
    parser.add_argument("--markdown", action="store_true", help="保存为 Markdown")
    parser.add_argument("--text-only", action="store_true", help="仅文本输出")
    parser.add_argument("--embed", action="store_true", help="显示 Discord 嵌入链接")
    parser.add_argument("--output-dir", default="data", help="输出目录")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.url:
        print("请提供 URL: python3 fetch.py --url <url>")
        return 1

    reader = XReader(args.output_dir)

    if args.embed:
        embed_url = reader.get_fxembed_url(args.url)
        print("Discord 嵌入链接:")
        print(f"<{embed_url}>")
        return 0

    parsed = reader.save(args.url, markdown=args.markdown)
    if parsed and args.text_only:
        print(reader.to_markdown(parsed) or "")

    return 0 if parsed else 1


if __name__ == "__main__":
    raise SystemExit(main())
