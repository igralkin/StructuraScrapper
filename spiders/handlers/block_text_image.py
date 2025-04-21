from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class BlockTextImage(BaseHandler):
    def name(self) -> str:
        return "block_text_image"

    def extract(self, html: str) -> dict | None:
        # Поиск блока текст + изображение
        soup = BeautifulSoup(html, "html.parser")
        container = soup.select_one(".block-text-image, .text-image, div.text_img")
        if not container:
            return None
        text = container.find("p") or container.find("div", class_="text")
        img = container.find("img")
        if img and text:
            return {
                "html": str(container),
                "text": text.get_text(strip=True),
                "image_src": img.get("src")
            }
        return None
    def find_all(self, soup):
        return soup.select(".block-text-image, .text-image, div.text_img")