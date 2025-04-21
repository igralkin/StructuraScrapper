from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class BlockImage2Col(BaseHandler):
    def name(self) -> str:
        return "block_image_2col"

    def find_all(self, soup):
        return soup.select(".two-col-image, .img-2col, .block-image-2col")

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        cont = soup.select_one(".two-col-image, .img-2col, .block-image-2col")
        if not cont:
            return None
        cols = cont.find_all(recursive=False)
        left = cols[0].find("img")
        right = cols[1]
        return {
            "html": str(cont),
            "image_src": left["src"] if left else None,
            "right_html": str(right)
        }
