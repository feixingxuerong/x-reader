import unittest

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from x_reader.url_utils import extract_tweet_id, find_x_urls, get_fxembed_url


class UrlUtilsTest(unittest.TestCase):
    def test_extract_tweet_id(self):
        url = "https://x.com/some_user/status/1234567890"
        self.assertEqual(extract_tweet_id(url), "1234567890")

    def test_fxembed_conversion(self):
        self.assertEqual(
            get_fxembed_url("https://x.com/user/status/1"),
            "https://fixupx.com/user/status/1",
        )
        self.assertEqual(
            get_fxembed_url("https://twitter.com/user/status/2"),
            "https://fxtwitter.com/user/status/2",
        )

    def test_find_urls(self):
        text = "a https://x.com/a/status/1 and https://twitter.com/b/status/2"
        urls = find_x_urls(text)
        self.assertEqual(len(urls), 2)


if __name__ == "__main__":
    unittest.main()
