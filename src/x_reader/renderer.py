"""Markdown rendering for parsed tweet structures."""

from __future__ import annotations

import re
from typing import Any


def _format_stats(stats: dict[str, Any]) -> str:
    parts: list[str] = []
    if stats.get("likes"):
        parts.append(f"❤️ {stats['likes']:,}")
    if stats.get("retweets"):
        parts.append(f"🔁 {stats['retweets']:,}")
    if stats.get("replies"):
        parts.append(f"💬 {stats['replies']:,}")
    if stats.get("views"):
        parts.append(f"👁️ {stats['views']:,}")
    return " | ".join(parts)


def to_markdown(parsed: dict[str, Any] | None) -> str | None:
    if not parsed:
        return None

    md: list[str] = []

    article = parsed.get("article")
    if article:
        md.append(f"# {article.get('title', 'Untitled')}")
        md.append("")
        md.append(f"*{parsed['author']['name']}*")
        md.append("")
        md.append("---")
        md.append("")
        md.append(article.get("content_text", ""))
        md.append("")
        md.append("---")
        md.append(f"🔗 [查看原文]({parsed['url']})")
        return "\n".join(md)

    author = parsed["author"]
    badge = " ✅" if author.get("verified") else ""
    if author.get("blue"):
        badge += " 💙"

    md.append(f"## 🐦 {author['name']}{badge}")
    md.append(f"**@{author['username']}**")
    md.append("")

    text = parsed.get("raw_text") or parsed.get("text", "")
    if text:
        text = re.sub(r"@(\w+)", r"**@\1**", text)
        text = re.sub(r"#(\w+)", r"**#\1**", text)
        text = re.sub(r"https?://\S+", "", text)
        md.append(text)
        md.append("")

    stats_str = _format_stats(parsed["stats"])
    if stats_str:
        md.append(stats_str)
        md.append("")

    if parsed.get("created_at"):
        md.append(f"*发布时间: {parsed['created_at']}*")

    md.append("")
    md.append(f"🔗 [查看原文]({parsed['url']})")
    return "\n".join(md)
