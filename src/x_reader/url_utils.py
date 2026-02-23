"""URL utilities for X/Twitter links."""

from __future__ import annotations

import re
from typing import Optional

# Keep username pattern broad enough to match common handles.
TWEET_ID_PATTERNS = [
    re.compile(r"twitter\.com/[A-Za-z0-9_]+/status/(\d+)", re.IGNORECASE),
    re.compile(r"x\.com/[A-Za-z0-9_]+/status/(\d+)", re.IGNORECASE),
    re.compile(r"twitter\.com/[A-Za-z0-9_]+/(\d+)", re.IGNORECASE),
    re.compile(r"x\.com/[A-Za-z0-9_]+/(\d+)", re.IGNORECASE),
]

X_URL_PATTERN = re.compile(
    r"(https?://(?:mobile\.)?(?:twitter|x)\.com/[A-Za-z0-9_]+/status/\d+)",
    re.IGNORECASE,
)


def extract_tweet_id(url: str) -> Optional[str]:
    """Extract tweet id from a URL, or return None when not found."""
    for pattern in TWEET_ID_PATTERNS:
        match = pattern.search(url)
        if match:
            return match.group(1)
    return None


def get_fxembed_url(url: str) -> str:
    """Convert x.com/twitter.com URL into FxEmbed-compatible URL."""
    result = url
    if "x.com" in result:
        return result.replace("x.com", "fixupx.com")
    if "twitter.com" in result:
        return result.replace("twitter.com", "fxtwitter.com")
    return result


def find_x_urls(text: str) -> list[str]:
    """Find all X/Twitter status URLs in a message."""
    return X_URL_PATTERN.findall(text or "")
