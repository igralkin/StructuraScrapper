from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class BlockContactForm(BaseHandler):
    def name(self) -> str:
        return "block_contact_form"

    def find_all(self, soup):
        return soup.select("form[action*='contact'], .contact-form, .feedback-form")

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        f = soup.select_one("form[action*='contact'], .contact-form, .feedback-form")
        if not f:
            return None
        fields = [inp.get("name") for inp in f.find_all("input") if inp.get("name")]
        return {"html": str(f), "fields": fields}
