from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class HeaderBitrix(BaseHandler):
    def name(self) -> str:
        return "header_bitrix"

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        header = soup.find(lambda tag: tag.name == "header" or (tag.get("class") and any("bitrix" in c for c in tag.get("class", []))))
        if header:
            return {"html": str(header)}
        return None