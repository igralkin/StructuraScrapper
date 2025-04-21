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

    def find_all(self, soup):
        found = soup.find_all("footer")
        if not found:
            found = soup.find_all(
                lambda tag: tag.name == "div"
                            and (
                                (tag.get("id") and "footer" in tag.get("id")) or
                                (tag.get("class") and any("footer" in c for c in tag.get("class")))
                            )
            )
        return found
