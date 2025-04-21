from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class BlockFormImage(BaseHandler):
    #Форма с картинкой
    def name(self) -> str:
        return "block_form_image"

    def find_all(self, soup):
        return soup.select(".form-image, .image-form, form:has(img)")

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        f = soup.find(lambda tag: tag.name=='form' and tag.find('img'))
        if not f:
            return None
        fields = [inp.get('name') for inp in f.find_all('input') if inp.get('name')]
        return {"html": str(f), "fields": fields}