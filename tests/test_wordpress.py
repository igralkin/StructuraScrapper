import unittest
from block_parser.parser import parse_blocks

WP_HTML = """
<!DOCTYPE html>
<html>
  <head><title>WP Site</title></head>
  <body>
    <header id="site-header" class="main-header">Header Content</header>
    <main>Main Content</main>
    <footer id="colophon" class="site-footer">Footer Content</footer>
  </body>
</html>
"""

class TestWordPressParser(unittest.TestCase):
    def test_parse_blocks_wordpress(self):
        result = parse_blocks(WP_HTML, cms="wordpress", url="https://wp-test.com")

        self.assertEqual(result['cms'], "wordpress")

        self.assertTrue(result['blocks']['header']['found'])
        self.assertIn("Header Content", result['blocks']['header']['content'])
        self.assertIn("strategy", result['blocks']['header'])

        self.assertTrue(result['blocks']['footer']['found'])
        self.assertIn("Footer Content", result['blocks']['footer']['content'])
        self.assertIn("strategy", result['blocks']['footer'])

if __name__ == '__main__':
    unittest.main()