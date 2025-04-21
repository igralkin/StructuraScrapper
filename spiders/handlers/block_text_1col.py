from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class BlockText1Col(BaseHandler):
    def name(self) -> str:
        return "block_text_1col"

    def extract(self, html: str) -> dict | None:
        # Одна колонка текста
        soup = BeautifulSoup(html, "html.parser")
        container = soup.select_one(".text-block, text-1col, article, div.text-block, div.block.text_banner")
        if not container:
            return None

        text = container.get_text(strip=True)
        if text and len(text) > 50:
            return {
                "html": str(container),
                "text": text
            }
        return None

    def find_all(self, soup):
        return soup.select(
            ".text-block, text-1col, article, div.text-block, div.block.text_banner"
        )