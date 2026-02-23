"""Persistence utilities for JSON and Markdown outputs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class DataStore:
    def __init__(self, data_dir: str = "data") -> None:
        self.data_dir = Path(data_dir)
        self.json_dir = self.data_dir / "json"
        self.markdown_dir = self.data_dir / "markdown"
        self.json_dir.mkdir(parents=True, exist_ok=True)
        self.markdown_dir.mkdir(parents=True, exist_ok=True)

    def save_json(self, tweet_id: str, data: dict[str, Any]) -> Path:
        name = tweet_id if str(tweet_id).startswith("tweet_") else f"tweet_{tweet_id}"
        path = self.json_dir / f"{name}.json"
        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        return path

    def save_markdown(self, tweet_id: str, markdown: str) -> Path:
        name = tweet_id if str(tweet_id).startswith("tweet_") else f"tweet_{tweet_id}"
        path = self.markdown_dir / f"{name}.md"
        with path.open("w", encoding="utf-8") as file:
            file.write(markdown)
        return path


# Backward compatibility for existing imports.
Storage = DataStore
