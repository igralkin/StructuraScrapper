from .base_handler import BaseHandler
from bs4 import BeautifulSoup
import re

class BlockTestimonial(BaseHandler):
    #Цитата и отзыв
    def name(self) -> str:
        return "block_testimonial"

    def find_all(self, soup):
        return soup.select(".testimonial, .quote, .reviews")

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        wrap = soup.select_one(".testimonial, .quote, .reviews")
        if not wrap:
            return None
        quote = wrap.find("blockquote") or wrap.find("p")
        author = wrap.find(class_=re.compile(r"author|cite"))
        return {"html": str(wrap), "quote": quote.get_text(strip=True) if quote else None, "author": author.get_text(strip=True) if author else None}