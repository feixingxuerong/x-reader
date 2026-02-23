import io
import unittest
from contextlib import redirect_stdout
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from x_reader.cli import main


class CliTest(unittest.TestCase):
    def test_embed_mode(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = main(["--embed", "--url", "https://x.com/u/status/123"])
        output = buf.getvalue()
        self.assertEqual(code, 0)
        self.assertIn("fixupx.com", output)

    def test_missing_url(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = main([])
        self.assertEqual(code, 1)
        self.assertIn("请提供 URL", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
