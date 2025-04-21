from .base_handler import BaseHandler
from bs4 import BeautifulSoup
import re

class BlockSearchResults(BaseHandler):
    def name(self) -> str:
        return "block_search_results"

    def find_all(self, soup):
        return soup.select(".search-results, .results-list")

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        wrap = soup.select_one(".search-results, .results-list")
        if not wrap:
            return None
        items = []
        for it in wrap.select(".result, .item"):
            title = it.find(re.compile("^h[1-6]$"))
            desc = it.find("p")
            items.append({
                "html": str(it),
                "title": title.get_text(strip=True) if title else None,
                "description": desc.get_text(strip=True) if desc else None
            })
        return {"html": str(wrap), "items": items}
