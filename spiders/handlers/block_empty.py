from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class BlockEmpty(BaseHandler):
    def name(self) -> str:
        return "block_empty"

    def find_all(self, soup):
        return [tag for tag in soup.find_all(True) if not tag.text.strip() and not tag.find(True)]

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        tag = soup.find(lambda t: not t.text.strip() and not t.find(True))
        return {"html": str(tag)} if tag else None