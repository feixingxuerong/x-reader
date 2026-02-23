import unittest

from x_reader.urls import extract_tweet_id, to_fxembed_url


class TestUrls(unittest.TestCase):
    def test_extract(self):
        self.assertEqual(extract_tweet_id("https://x.com/abc/status/123"), "123")
        self.assertEqual(extract_tweet_id("https://twitter.com/abc/status/456"), "456")
        self.assertIsNone(extract_tweet_id("https://example.com"))

    def test_fx(self):
        self.assertIn("fixupx.com", to_fxembed_url("https://x.com/a/status/1"))
        self.assertIn("fxtwitter.com", to_fxembed_url("https://twitter.com/a/status/1"))


if __name__ == "__main__":
    unittest.main()
