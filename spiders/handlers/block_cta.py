import re

from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class BlockCTA(BaseHandler):
    #Блок текст + действие
    def name(self) -> str:
        return "block_cta"

    def find_all(self, soup):
        return soup.select(".block.text_banner, .cta-block, .call-to-action")

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        cont = soup.select_one(".block.text_banner, cta-block, .call-to-action")
        if not cont:
            return None

        heading = cont.find(re.compile("^h[1-6]$"))
        paragraph = cont.find("p")
        button = cont.find("button")
        link = cont.find("a", href=True)

        data = {}
        if heading: data["heading"] = heading.get_text(strip=True)
        if paragraph: data["text"] = paragraph.get_text(strip=True)
        if button: button["button"] = button.get_text(strip=True)
        if link: data["url"] = link["href"]
        data["html"] = str(cont)
        return data
