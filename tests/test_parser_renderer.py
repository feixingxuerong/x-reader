import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from x_reader.parser import parse_tweet
from x_reader.renderer import to_markdown


class ParserRendererTest(unittest.TestCase):
    def setUp(self):
        self.sample = {
            "tweet": {
                "id": "42",
                "url": "https://x.com/u/status/42",
                "text": "hello @alice #python https://x.com/u/status/42",
                "raw_text": {"text": "hello @alice #python"},
                "created_at": "2026-02-23T00:00:00Z",
                "author": {
                    "id": "1",
                    "name": "Tester",
                    "screen_name": "tester",
                    "verified": True,
                    "blue": True,
                },
                "likes": 100,
                "retweets": 20,
                "replies": 3,
                "views": 999,
            }
        }

    def test_parse_tweet(self):
        parsed = parse_tweet(self.sample)
        self.assertEqual(parsed["id"], "42")
        self.assertEqual(parsed["author"]["username"], "tester")

    def test_render_markdown(self):
        parsed = parse_tweet(self.sample)
        md = to_markdown(parsed)
        self.assertIn("## 🐦 Tester", md)
        self.assertIn("**@alice**", md)
        self.assertIn("**#python**", md)
        self.assertIn("🔗 [查看原文](https://x.com/u/status/42)", md)


if __name__ == "__main__":
    unittest.main()
