from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class BlockFormText(BaseHandler):
    #Форма с текстом
    def name(self) -> str:
        return "block_form_text"

    def find_all(self, soup):
        return soup.select(".form-text, .text-form, form:has(textarea)")

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        f = soup.find(lambda tag: tag.name=='form' and tag.find('textarea'))
        if not f:
            return None
        fields = [inp.get('name') for inp in f.find_all(['input','textarea']) if inp.get('name')]
        return {"html": str(f), "fields": fields}
