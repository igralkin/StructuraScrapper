from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class BlockImage3Col(BaseHandler):
    def name(self) -> str:
        return "block_image_3col"

    def find_all(self, soup):
        return soup.select(".three-col-image, .img-3col, .block-image-3col")

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        cont = soup.select_one(".three-col-image, .img-3col, .block-image-3col")
        if not cont:
            return None
        parts = cont.find_all(recursive=False)
        return {
            "html": str(cont),
            "cols": [str(p) for p in parts[:3]]
        }
