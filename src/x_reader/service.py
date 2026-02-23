from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, Optional

from .client import FxTwitterClient
from .formatter import to_markdown
from .parser import parse_tweet_payload
from .storage import Storage
from .urls import extract_tweet_id, to_fxembed_url


class XReader:
    """对外门面（保持与旧版 fetch.py 的类名一致）。"""

    def __init__(self, data_dir: str = "data", client: FxTwitterClient | None = None):
        self.storage = Storage(data_dir)
        self.client = client or FxTwitterClient()

    def extract_tweet_id(self, url: str) -> str | None:
        return extract_tweet_id(url)

    def get_fxembed_url(self, url: str) -> str:
        return to_fxembed_url(url)

    def fetch_tweet(self, url: str):
        tid = extract_tweet_id(url)
        if not tid:
            return None
        return self.client.fetch_status(tid)

    def parse_tweet(self, data: Dict[str, Any] | None):
        return parse_tweet_payload(data)

    def to_markdown(self, parsed) -> str | None:
        if not parsed:
            return None
        return to_markdown(parsed)

    def save(self, url: str, markdown: bool = True, json_save: bool = True):
        data = self.fetch_tweet(url)
        if not data:
            return None
        parsed = self.parse_tweet(data)
        if not parsed:
            return None

        filename = f"tweet_{parsed.id}"

        if json_save:
            self.storage.save_json(filename, data)
        if markdown:
            md = self.to_markdown(parsed) or ""
            self.storage.save_markdown(filename, md)

        return parsed
