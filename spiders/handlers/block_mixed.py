from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class BlockMixed(BaseHandler):
    def name(self) -> str:
        return "block_mixed"

    def find_all(self, soup):
        return soup.select(".mixed-content, .mixed-block")

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        m = soup.select_one(".mixed-content, .mixed-block")
        if not m:
            return None
        return {"html": str(m)}
