import re

from .base_handler import BaseHandler
from bs4 import BeautifulSoup


class BlockPopup(BaseHandler):
    def name(self) -> str:
        return "block_popup"

    def extract(self, html: str) -> dict | None:
        # Попап, виджет
        soup = BeautifulSoup(html, "html.parser")
        elm = soup.find(attrs={"data-modal": True})or soup.select_one(".popup, .modal, .widget")
        if not elm:
            return None
        title = elm.find(re.compile("^h[1-6]$"))
        body = elm.find("p")
        return {
            "html": str(elm),
            "title": title.get_text(strip=True) if title else None,
            "text": body.get_text(strip=True) if body else None
        }

    def find_all(self, soup):
        return soup.select("[data-modal], .popup, .modal, .widget")