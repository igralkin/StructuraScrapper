from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class BlockPartners(BaseHandler):
    def name(self) -> str:
        return "block_partners"

    def find_all(self, soup):
        return soup.select(".partners, .our-partners, .partners-list")

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        wrap = soup.select_one(".partners, .our-partners, .partners-list")
        if not wrap:
            return None
        logos = wrap.select("img")
        urls = [img.get("src") for img in logos]
        return {"html": str(wrap), "logos": urls}
