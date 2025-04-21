from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class BlocText2Col(BaseHandler):
    def name(self) -> str:
        return "block_text_2col"

    def find_all(self, soup):
        return soup.select(".text-2col, .two-cols-text, .text_block_2col")

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        cont = soup.select_one(".text-2col, .two-cols-text, .text_block_2col")
        if not cont:
            return None
        cols = [c.get_text(strip=True) for c in cont.find_all(["p", "div"], recursive=False)]
        return {
            "html": str(cont),
            "columns": cols
        }