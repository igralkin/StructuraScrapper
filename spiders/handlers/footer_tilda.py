from .base_handler import BaseHandler
from bs4 import BeautifulSoup
import re

class FooterTilda(BaseHandler):
    def name(self) -> str:
        return "footer_tilda"

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        footer = soup.find(lambda tag: tag.name == "footer" or tag.get("class") and any(re.match(r"t-\d+header", c) for c in tag.get("class", [])))
        if footer:
            return {"html": str(footer)}
        return None