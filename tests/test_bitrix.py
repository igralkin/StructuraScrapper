import unittest
from block_parser.parser import parse_blocks

BITRIX_HTML = """
<html>
  <body>
    <div class="bx-layout bx-header">Header Bitrix</div>
    <main>Main content</main>
    <div class="adm-footer bx-footer">Footer Bitrix</div>
  </body>
</html>
"""


class TestBitrixParser(unittest.TestCase):
    def test_parse_blocks_bitrix(self):
        result = parse_blocks(BITRIX_HTML, cms="bitrix", url="https://bitrix-test.com")

        self.assertEqual(result['cms'], "bitrix")

        self.assertTrue(result['blocks']['header']['found'])
        self.assertIn("Header Bitrix", result['blocks']['header']['content'])
        self.assertIn("strategy", result['blocks']['header'])

        self.assertTrue(result['blocks']['footer']['found'])
        self.assertIn("Footer Bitrix", result['blocks']['footer']['content'])
        self.assertIn("strategy", result['blocks']['footer'])


if __name__ == '__main__':
    unittest.main()
