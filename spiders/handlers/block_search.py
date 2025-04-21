from .base_handler import BaseHandler
from bs4 import BeautifulSoup
import re

class BlockSearch(BaseHandler):
    def name(self) -> str:
        return "block_search"

    def find_all(self, soup):
        return soup.select("form[action*='/search'], .search-bar, .search-form")

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        form = soup.find("form", action=re.compile(r"/search"))
        if not form:
            return None
        inp = form.find("input", {"type": "search"}) or form.find("input", {"name": "q"})
        return {
            "html": str(form),
            "placeholder": inp.get("placeholder") if inp else None
        }
