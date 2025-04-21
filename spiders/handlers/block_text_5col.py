from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class BlocText5Col(BaseHandler):
    def name(self) -> str:
        return "block_text_5col"

    def find_all(self, soup):
        return soup.select(".text-5col, .five-cols-text, .text_block_5col")

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        cont = soup.select_one(".text-5col, .five-cols-text, .text_block_5col")
        if not cont:
            return None
        texts = [c.get_text(strip=True) for c in cont.find_all(["p", "div"], recursive=False)][:5]
        return {
            "html": str(cont),
            "columns": texts
        }