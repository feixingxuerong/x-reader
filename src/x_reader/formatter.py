from __future__ import annotations

import re

from .models import Tweet


def _fmt_int(n):
    try:
        return f"{int(n):,}"
    except Exception:
        return None


def to_markdown(tweet: Tweet) -> str:
    # Article
    if tweet.article:
        a = tweet.article
        return "\n".join([
            f"# {a.title}",
            "",
            f"*{tweet.author.name}*",
            "",
            "---",
            "",
            a.content_text,
            "",
            "---",
            f"🔗 [查看原文]({tweet.url})",
        ])

    md = []
    badge = " ✅" if tweet.author.verified else ""
    if tweet.author.blue:
        badge += " 💙"

    md.append(f"## 🐦 {tweet.author.name}{badge}")
    md.append(f"**@{tweet.author.username}**")
    md.append("")

    text = tweet.raw_text or tweet.text
    if text:
        text = re.sub(r"@(\w+)", r"**@\1**", text)
        text = re.sub(r"#(\w+)", r"**#\1**", text)
        text = re.sub(r"https?://\S+", r"", text)
        md.append(text.strip())
        md.append("")

    parts = []
    if tweet.stats.likes:
        parts.append(f"❤️ {_fmt_int(tweet.stats.likes)}")
    if tweet.stats.retweets:
        parts.append(f"🔁 {_fmt_int(tweet.stats.retweets)}")
    if tweet.stats.replies:
        parts.append(f"💬 {_fmt_int(tweet.stats.replies)}")
    if tweet.stats.views:
        parts.append(f"👁️ {_fmt_int(tweet.stats.views)}")

    if parts:
        md.append(" | ".join(parts))
        md.append("")

    if tweet.created_at:
        md.append(f"*发布时间: {tweet.created_at}*")

    md.append("")
    md.append(f"🔗 [查看原文]({tweet.url})")

    return "\n".join(md)
