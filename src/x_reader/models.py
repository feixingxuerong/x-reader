from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class Author:
    id: Optional[str]
    name: str
    username: str
    avatar_url: Optional[str] = None
    verified: bool = False
    blue: bool = False


@dataclass
class Stats:
    likes: Optional[int] = None
    retweets: Optional[int] = None
    replies: Optional[int] = None
    views: Optional[int] = None


@dataclass
class Article:
    id: Optional[str]
    title: str
    preview_text: str
    content_text: str
    created_at: Optional[str]
    blocks: List[Dict[str, Any]]


@dataclass
class Tweet:
    id: str
    url: str
    text: str
    raw_text: str
    created_at: Optional[str]
    author: Author
    stats: Stats
    media: List[Dict[str, Any]]
    entities: Dict[str, Any]
    is_note_tweet: bool = False
    article: Optional[Article] = None
