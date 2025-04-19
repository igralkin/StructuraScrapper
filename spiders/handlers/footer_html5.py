from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class FooterHTML5(BaseHandler):
    def name(self) -> str:
        return "footer_html5"

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        footer = soup.find("footer")
        if footer:
            return {"html": str(footer)}
        return None