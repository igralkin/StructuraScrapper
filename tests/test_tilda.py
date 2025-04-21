import unittest
from block_parser.parser import parse_blocks

TILDA_HTML = """
<html>
  <body>
    <div class="t123-rec t123-r t123-header" id="rec123">Header from Tilda</div>
    <div>Main content</div>
    <div class="t456-rec t456-r t456-footer" id="rec456">Footer from Tilda</div>
  </body>
</html>
"""


class TestTildaParser(unittest.TestCase):
    def test_parse_blocks_tilda(self):
        result = parse_blocks(TILDA_HTML, cms="tilda", url="https://tilda-test.com")

        self.assertEqual(result['cms'], "tilda")

        self.assertTrue(result['blocks']['header']['found'])
        self.assertIn("Header from Tilda", result['blocks']['header']['content'])
        self.assertIn("strategy", result['blocks']['header'])

        self.assertTrue(result['blocks']['footer']['found'])
        self.assertIn("Footer from Tilda", result['blocks']['footer']['content'])
        self.assertIn("strategy", result['blocks']['footer'])


if __name__ == '__main__':
    unittest.main()
