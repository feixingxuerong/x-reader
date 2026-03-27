import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from x_reader.reader import XReader


class FakeClient:
    def fetch_tweet(self, url):
        return {
            "tweet": {
                "id": "7",
                "url": url,
                "text": "plain text",
                "raw_text": {"text": "plain text"},
                "author": {"name": "A", "screen_name": "a"},
                "likes": 1,
                "retweets": 2,
                "replies": 3,
                "views": 4,
            }
        }


class ReaderSaveTest(unittest.TestCase):
    def test_save_outputs_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            reader = XReader(data_dir=tmp, client=FakeClient())
            parsed = reader.save("https://x.com/a/status/7", markdown=True, json_save=True)
            self.assertIsNotNone(parsed)

            json_path = Path(tmp) / "json" / "tweet_7.json"
            md_path = Path(tmp) / "markdown" / "tweet_7.md"
            self.assertTrue(json_path.exists())
            self.assertTrue(md_path.exists())


if __name__ == "__main__":
    unittest.main()
