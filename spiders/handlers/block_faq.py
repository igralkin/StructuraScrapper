from .base_handler import BaseHandler
from bs4 import BeautifulSoup
import re

class BlockFAQ(BaseHandler):
    def name(self) -> str:
        return "block_faq"

    def find_all(self, soup):
        return soup.select(".faq, .accordion, .question-list")

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        wrap = soup.select_one(".faq, .accordion, .question-list")
        if not wrap:
            return None
        items = []
        for item in wrap.select(".faq-item, .question"):
            q = item.find(re.compile(r"^h[1-6]$"))
            a = item.find("p, .answer")
            items.append({"question": q.get_text(strip=True) if q else None, "answer": a.get_text(strip=True) if a else None})
        return {"html": str(wrap), "items": items}