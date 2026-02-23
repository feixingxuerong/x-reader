"""Parsing helpers for FxTwitter payloads."""

from __future__ import annotations

from typing import Any


def parse_article(article: dict[str, Any] | None) -> dict[str, Any] | None:
    if not article:
        return None

    content_text = ""
    blocks = article.get("content", {}).get("blocks", [])
    for block in blocks:
        block_type = block.get("type", "")
        block_text = block.get("text", "")

        if block_type == "header-one":
            content_text += f"# {block_text}\n\n"
        elif block_type == "header-two":
            content_text += f"## {block_text}\n\n"
        elif block_type == "blockquote":
            content_text += f"> {block_text}\n\n"
        elif block_type == "unstyled":
            content_text += f"{block_text}\n\n"
        elif block_type == "atomic":
            media = block.get("data", {})
            if media.get("entityKey"):
                content_text += "[媒体内容]\n\n"
        elif block_text:
            content_text += f"{block_text}\n\n"

    return {
        "id": article.get("id"),
        "title": article.get("title"),
        "preview_text": article.get("preview_text"),
        "content_text": content_text.strip(),
        "created_at": article.get("created_at"),
        "blocks": blocks,
    }


def parse_tweet(data: dict[str, Any] | None) -> dict[str, Any] | None:
    if not data or "tweet" not in data:
        return None

    tweet = data["tweet"]
    author = tweet.get("author", {})

    result = {
        "id": tweet.get("id"),
        "url": tweet.get("url"),
        "text": tweet.get("text"),
        "raw_text": tweet.get("raw_text", {}).get("text", ""),
        "created_at": tweet.get("created_at"),
        "author": {
            "id": author.get("id"),
            "name": author.get("name"),
            "username": author.get("screen_name"),
            "avatar_url": author.get("avatar_url"),
            "verified": author.get("verified", False),
            "blue": author.get("blue", False),
        },
        "stats": {
            "likes": tweet.get("likes"),
            "retweets": tweet.get("retweets"),
            "replies": tweet.get("replies"),
            "views": tweet.get("views"),
        },
        "media": tweet.get("media", []),
        "entities": tweet.get("entities", {}),
        "is_note_tweet": tweet.get("is_note_tweet", False),
    }

    if tweet.get("article"):
        result["article"] = parse_article(tweet["article"])

    return result


# Backward compatibility alias for older modules.
parse_tweet_payload = parse_tweet
