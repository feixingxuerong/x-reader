import unittest
import sys
from pathlib import Path

# Ensure `src/` is importable when tests are run standalone.
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


from x_reader.service import XReader


class TestSmoke(unittest.TestCase):
    def test_embed(self):
        r = XReader("/tmp/x-reader-test")
        self.assertTrue(r.get_fxembed_url("https://x.com/a/status/1").startswith("https://"))


if __name__ == "__main__":
    unittest.main()
