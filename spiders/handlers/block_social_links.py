from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class BlockSocialLinks(BaseHandler):
    def name(self) -> str:
        return "block_social_links"

    def find_all(self, soup):
        return soup.select(".social-links, .social, a[href*='facebook'], a[href*='twitter'], a[href*='instagram']")

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        links = soup.select(".social-links a, .social a")
        urls = [a["href"] for a in links if a.get("href")]
        return {"html": str(soup), "urls": urls}