from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class HeaderHTML5(BaseHandler):
    def name(self) -> str:
        return "header_html5"

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        header = soup.find("header")
        if header:
            return {"html": str(header)}
        return None

    def find_all(self, soup):
        return soup.find_all("header")