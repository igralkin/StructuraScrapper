import linecache

from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class BlockList(BaseHandler):
    #Списки
    def name(self) -> str:
        return "block_list"

    def find_all(self, soup):
        return soup.select("ul, ol")

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        lst = soup.find(["ul", "ol"])
        if not lst or not lst.find_all("li"):
            return None

        items = [li.get_text(strip=True) for li in lst.find_all("li")]
        return {
            "html": str(lst),
            "items": items
        }