from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class BlockCarousel(BaseHandler):
    def name(self) -> str:
        return "block_carousel"

    def find_all(self, soup):
        return soup.select(".carousel, .slider, .slides")

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        slider = soup.select_one(".carousel, .slider, .slides")
        if not slider:
            return None

        slides = []
        for slide in slider.select(".slide, li, .slick-slide"):
            img = slide.find("img")
            desc = slide.find("p") or slide.get_text(strip=True)
            slides.append({
                "html": str(slide),
                "image": img["src"] if img else None,
                "text": desc.strip() if desc else None
            })
        if not slides:
            return None
        return {"html": str(slider), "slides": slides}