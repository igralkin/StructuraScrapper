from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class FooterWP(BaseHandler):
    def name(self) -> str:
        return "header_wp"

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        footer = soup.select_one("footer.wp-footer, footer.site-footer, div#colophon")
        if footer:
            return {"html": str(footer)}
        return None