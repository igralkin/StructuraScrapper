from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class BlockImage(BaseHandler):
    def name(self) -> str:
        return "block_image"

    def extract(self, html: str) -> dict | None:
        # Поиск блока c изображением
        soup = BeautifulSoup(html, "html.parser")
        cont = soup.select_one(".image-block, .block-img, .img-only")
        if not cont:
            return None
        img = cont.find("img")
        caption = cont.find("figcaption") or cont.find("p")
        return {
            "html": str(cont),
            "src": img["src"] if img else None,
            "alt": img.get("alt") if img else None,
            "caption": caption.get_text(strip=True) if caption else None
        }

    def find_all(self, soup):
        return soup.select(".image-block, .block-img, .img-only")