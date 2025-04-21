from .base_handler import BaseHandler
from bs4 import BeautifulSoup
import re

class BlockProducts(BaseHandler):
    def name(self) -> str:
        return "block_products"

    def find_all(self, soup):
        return soup.select(".products-list, .products, .catalog")

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        wrap = soup.select_one(".products-list, .products, .catalog")
        if not wrap:
            return None
        cards = wrap.select(".product-card, .card-product, .item-card")
        items = []
        for c in cards:
            title = c.find(re.compile("^h[1-6]$"))
            price = c.find(class_=re.compile("price"))
            img = c.find("img")
            items.append({
                "html": str(c),
                "title": title.get_text(strip=True) if title else None,
                "price": price.get_text(strip=True) if price else None,
                "image": img["src"] if img else None
            })
        return {"html": str(wrap), "items": items}
