from __future__ import annotations

from typing import Any, Dict, List, Optional

from .models import Article, Author, Stats, Tweet


def parse_article(article: Dict[str, Any] | None) -> Article | None:
    if not article:
        return None

    content_text = ""
    blocks = (article.get("content") or {}).get("blocks") or []
    for b in blocks:
        t = b.get("type") or ""
        txt = b.get("text") or ""
        if not txt and t != "atomic":
            continue
        if t == "header-one":
            content_text += f"# {txt}\n\n"
        elif t == "header-two":
            content_text += f"## {txt}\n\n"
        elif t == "blockquote":
            content_text += f"> {txt}\n\n"
        elif t == "unstyled":
            content_text += f"{txt}\n\n"
        elif t == "atomic":
            content_text += "[媒体内容]\n\n"
        else:
            content_text += f"{txt}\n\n"

    return Article(
        id=article.get("id"),
        title=article.get("title") or "Untitled",
        preview_text=article.get("preview_text") or "",
        content_text=content_text.strip(),
        created_at=article.get("created_at"),
        blocks=blocks,
    )


def parse_tweet_payload(data: Dict[str, Any] | None) -> Tweet | None:
    if not data or "tweet" not in data:
        return None

    tweet = data["tweet"]
    author = tweet.get("author") or {}

    a = Author(
        id=author.get("id"),
        name=author.get("name") or "",
        username=author.get("screen_name") or "",
        avatar_url=author.get("avatar_url"),
        verified=bool(author.get("verified", False)),
        blue=bool(author.get("blue", False)),
    )

    s = Stats(
        likes=tweet.get("likes"),
        retweets=tweet.get("retweets"),
        replies=tweet.get("replies"),
        views=tweet.get("views"),
    )

    article = parse_article(tweet.get("article"))

    return Tweet(
        id=str(tweet.get("id")),
        url=tweet.get("url") or "",
        text=tweet.get("text") or "",
        raw_text=((tweet.get("raw_text") or {}).get("text")) or "",
        created_at=tweet.get("created_at"),
        author=a,
        stats=s,
        media=tweet.get("media") or [],
        entities=tweet.get("entities") or {},
        is_note_tweet=bool(tweet.get("is_note_tweet", False)),
        article=article,
    )
