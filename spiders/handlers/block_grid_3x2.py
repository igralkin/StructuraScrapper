from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class BlockGrid3x2(BaseHandler):
    def name(self) -> str:
        return "block_grid_3x2"

    def find_all(self, soup):
        return soup.select(".grid-3x2, .elements-3x2")

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        g = soup.select_one(".grid-3x2, .elements-3x2")
        if not g:
            return None
        elems = g.find_all(recursive=False)
        return {"html": str(g), "elements": [str(e) for e in elems][:6]}
