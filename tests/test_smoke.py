import unittest

from x_reader.service import XReader


class TestSmoke(unittest.TestCase):
    def test_embed(self):
        r = XReader("/tmp/x-reader-test")
        self.assertTrue(r.get_fxembed_url("https://x.com/a/status/1").startswith("https://"))


if __name__ == "__main__":
    unittest.main()
