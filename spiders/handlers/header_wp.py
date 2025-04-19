from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class HeaderWP(BaseHandler):
    def name(self) -> str:
        return "header_wp"

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        header = soup.select_one("header.wp-header, header.site-header, div#masthead")
        if header:
            return {"html": str(header)}
        return None