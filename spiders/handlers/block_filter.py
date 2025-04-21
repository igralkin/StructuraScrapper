from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class BlockFilter(BaseHandler):
    def name(self) -> str:
        return "block_filter"

    def find_all(self, soup):
        return soup.select(".filter, .filters, .filter-bar")

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        filt = soup.select_one(".filter, .filters, .filter-bar")
        if not filt:
            return None
        options = [opt.get_text(strip=True) for opt in filt.select("select option, .option")]
        return {"html": str(filt), "options": options}