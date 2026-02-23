from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

import requests


@dataclass
class FxTwitterClient:
    base_url: str = "https://api.fxtwitter.com"
    timeout: int = 30

    def fetch_status(self, tweet_id: str) -> Dict[str, Any] | None:
        url = f"{self.base_url}/status/{tweet_id}"
        try:
            r = requests.get(url, timeout=self.timeout)
            r.raise_for_status()
            return r.json()
        except requests.RequestException:
            return None
