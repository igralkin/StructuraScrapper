from .base_handler import BaseHandler
from bs4 import BeautifulSoup
import re

class BlockMap(BaseHandler):
    def name(self) -> str:
        return "block_map"

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        frame = soup.find("iframe", src=re.compile(r"google\.com/maps"))
        if frame:
            return {"html": str(frame), "src": frame["src"]}
        div = soup.select_one(".map, .map-container")
        return {"html": str(div)} if div else None

    def find_all(self, soup):
        return soup.select('iframe[src*="google.com/maps"], .map, .map-container')