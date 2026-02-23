"""API client for fetching tweet payloads from FxTwitter."""

from __future__ import annotations

from typing import Any

import requests

from .url_utils import extract_tweet_id


class FxTwitterClient:
    """Thin client for https://api.fxtwitter.com."""

    API_BASE = "https://api.fxtwitter.com/status"

    def __init__(self, timeout: int = 30):
        self.timeout = timeout

    def fetch_status(self, tweet_id: str) -> dict[str, Any] | None:
        """Compatibility method used by older service module."""
        api_url = f"{self.API_BASE}/{tweet_id}"
        try:
            response = requests.get(api_url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return None

    def fetch_tweet(self, url: str) -> dict[str, Any]:
        tweet_id = extract_tweet_id(url)
        if not tweet_id:
            raise ValueError(f"无法从 URL 中提取推文 ID: {url}")

        api_url = f"{self.API_BASE}/{tweet_id}"
        response = requests.get(api_url, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
