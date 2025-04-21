from .base_handler import BaseHandler
from bs4 import BeautifulSoup
import re

class BlockProductCard(BaseHandler):
    def name(self) -> str:
        return "block_product_card"

    def find_all(self, soup):
        return soup.select(".product-card, .card-product, .item-card")

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        card = soup.select_one(".product-card, .card-product, .item-card")
        if not card:
            return None
        title = card.find(re.compile("^h[1-6]$"))
        price = card.find(class_=re.compile("price"))
        img = card.find("img")
        return {
            "html": str(card),
            "title": title.get_text(strip=True) if title else None,
            "price": price.get_text(strip=True) if price else None,
            "image": img["src"] if img else None
        }
