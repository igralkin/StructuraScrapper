import unittest
from block_parser.parser import parse_blocks

HTML5_HTML = """
<html>
  <body>
    <header>Simple HTML5 Header</header>
    <main>Main content</main>
    <footer>Simple HTML5 Footer</footer>
  </body>
</html>
"""


class TestHTML5Parser(unittest.TestCase):
    def test_parse_blocks_html5(self):
        result = parse_blocks(HTML5_HTML, cms="html5", url="https://html5-test.com")

        self.assertEqual(result['cms'], "html5")

        self.assertTrue(result['blocks']['header']['found'])
        self.assertIn("HTML5 Header", result['blocks']['header']['content'])

        self.assertTrue(result['blocks']['footer']['found'])
        self.assertIn("HTML5 Footer", result['blocks']['footer']['content'])


if __name__ == '__main__':
    unittest.main()
