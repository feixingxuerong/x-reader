"""High-level XReader facade orchestrating fetch/parse/render/save."""

from __future__ import annotations

from typing import Any

import requests

from .client import FxTwitterClient
from .parser import parse_tweet
from .renderer import to_markdown
from .storage import DataStore
from .url_utils import extract_tweet_id, get_fxembed_url


class XReader:
    """X/Twitter 内容读取器。"""

    def __init__(self, data_dir: str = "data", client: FxTwitterClient | None = None):
        self.store = DataStore(data_dir)
        self.client = client or FxTwitterClient()

    def extract_tweet_id(self, url: str) -> str | None:
        return extract_tweet_id(url)

    def get_fxembed_url(self, url: str) -> str:
        return get_fxembed_url(url)

    def fetch_tweet(self, url: str, text_only: bool = False) -> dict[str, Any] | None:
        _ = text_only  # Backward-compatible argument; not used in API call.
        try:
            return self.client.fetch_tweet(url)
        except (ValueError, requests.RequestException) as exc:
            print(f"获取推文失败: {exc}")
            return None

    def parse_tweet(self, data: dict[str, Any] | None) -> dict[str, Any] | None:
        return parse_tweet(data)

    def to_markdown(self, parsed: dict[str, Any] | None) -> str | None:
        return to_markdown(parsed)

    def save(self, url: str, markdown: bool = True, json_save: bool = True) -> dict[str, Any] | None:
        data = self.fetch_tweet(url)
        if not data:
            return None

        parsed = self.parse_tweet(data)
        if not parsed:
            return None

        tweet_id = parsed["id"]

        if json_save:
            json_path = self.store.save_json(tweet_id, data)
            print(f"JSON 已保存: {json_path}")

        if markdown:
            markdown_content = self.to_markdown(parsed)
            md_path = self.store.save_markdown(tweet_id, markdown_content or "")
            print(f"Markdown 已保存: {md_path}")

        return parsed
