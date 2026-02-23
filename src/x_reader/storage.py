from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict

from .models import Tweet


class Storage:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.json_dir = self.data_dir / "json"
        self.md_dir = self.data_dir / "markdown"
        self.json_dir.mkdir(parents=True, exist_ok=True)
        self.md_dir.mkdir(parents=True, exist_ok=True)

    def save_json(self, filename: str, payload: Dict[str, Any]) -> Path:
        p = self.json_dir / f"{filename}.json"
        p.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return p

    def save_markdown(self, filename: str, markdown: str) -> Path:
        p = self.md_dir / f"{filename}.md"
        p.write_text(markdown, encoding="utf-8")
        return p
