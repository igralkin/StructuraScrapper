import unittest
from block_parser.parser import parse_blocks

DRUPAL_HTML = """
<html>
  <body>
    <div id="branding" class="region-header block-system-branding">Drupal Header</div>
    <main>Main content</main>
    <div id="footer" class="region-footer">Drupal Footer</div>
  </body>
</html>
"""


class TestDrupalParser(unittest.TestCase):
    def test_parse_blocks_drupal(self):
        result = parse_blocks(DRUPAL_HTML, cms="drupal", url="https://drupal-test.com")

        self.assertEqual(result['cms'], "drupal")

        self.assertTrue(result['blocks']['header']['found'])
        self.assertIn("Drupal Header", result['blocks']['header']['content'])
        self.assertIn("strategy", result['blocks']['header'])

        self.assertTrue(result['blocks']['footer']['found'])
        self.assertIn("Drupal Footer", result['blocks']['footer']['content'])
        self.assertIn("strategy", result['blocks']['footer'])


if __name__ == '__main__':
    unittest.main()
    