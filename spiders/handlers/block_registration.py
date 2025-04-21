from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class BlockRegistration(BaseHandler):
    def name(self) -> str:
        return "block_registration"

    def find_all(self, soup):
        return soup.select(".registration, .signup-form, form[action*='register']")

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        cont = soup.select_one(".registration, .signup-form, form[action*='register']")
        if not cont:
            return None
        fields = [inp.get('name') for inp in cont.find_all('input') if inp.get('name')]
        return {"html": str(cont), "fields": fields}