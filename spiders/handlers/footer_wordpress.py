from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class FooterWP(BaseHandler):
    def name(self) -> str:
        return "footer_wordpress"

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        footer = soup.select_one("footer.wp-footer, footer.site-footer, div#colophon")
        if footer:
            return {"html": str(footer)}
        return None

    def find_all(self, soup):
        found = soup.select("footer.wp-footer, footer.site-footer, div#colophon")
        if not found:
            found = soup.find_all("footer")
        return found
