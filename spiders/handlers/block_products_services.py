import re

from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class BlockProductsServices(BaseHandler):
    #Товары и услуги
    def name(self) -> str:
        return "block_products_services"

    def find_all(self, soup):
        return soup.select(".products, .services-list, .catalog")

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        cont = soup.select_one(".products, .services-list, .catalog")
        if not cont:
            return None

        items = []
        for item in cont.select(".product, .item, li"):
            title = item.find(re.compile("^h[1-6]$"))
            price = item.find(class_=re.compile("price|cost"))
            items.append({
                "html": str(item),
                "title": title.get_text(strip=True) if title else None,
                "price": price.get_text(strip=True) if price else None
            })
        if not items:
            return None
        return {"html": str(cont), "items": items}