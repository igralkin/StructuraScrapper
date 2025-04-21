from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class BlockCarouselText(BaseHandler):
    def name(self) -> str:
        return "block_carousel_text"

    def find_all(self, soup):
        return soup.select(".carousel-text, .slider-text, .text-slideshow")

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        c = soup.select_one(".carousel-text, .slider-text, .text-slideshow")
        if not c:
            return None
        slides = []
        for slide in c.select(".slide, .item"):
            text = slide.get_text(strip=True)
            slides.append({"html": str(slide), "text": text})
        return {"html": str(c), "slides": slides}
