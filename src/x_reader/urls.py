from __future__ import annotations

import re


_TWEET_ID_PATTERNS = [
    r"twitter\.com/\w+/status/(\d+)",
    r"x\.com/\w+/status/(\d+)",
    r"twitter\.com/\w+/(\d+)",
    r"x\.com/\w+/(\d+)",
]


def extract_tweet_id(url: str) -> str | None:
    for p in _TWEET_ID_PATTERNS:
        m = re.search(p, url)
        if m:
            return m.group(1)
    return None


def to_fxembed_url(url: str) -> str:
    if "x.com" in url:
        return url.replace("x.com", "fixupx.com")
    if "twitter.com" in url:
        return url.replace("twitter.com", "fxtwitter.com")
    return url
