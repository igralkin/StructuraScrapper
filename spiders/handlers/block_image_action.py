from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class BlockImageAction(BaseHandler):
    def name(self) -> str:
        return "block_image_action"

    def find_all(self, soup):
        return soup.select(".img-action, .image-with-button, .block-img-action")

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        cont = soup.select_one(".img-action, .image-with-button, .block-img-action")
        if not cont:
            return None
        img = cont.find("img")
        btn = cont.find("button") or cont.find("a", role="button")
        return {
            "html": str(cont),
            "image_src": img["src"] if img else None,
            "action": btn.get_text(strip=True) if btn else None
        }
