from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class BlockFormVideo(BaseHandler):
    #Форма с видео
    def name(self) -> str:
        return "block_form_video"

    def find_all(self, soup):
        return soup.select(".form-video, .video-form, form:has(video), form:has(iframe[src*='youtube'])")

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        f = soup.find(lambda tag: tag.name=='form' and (tag.find('video') or tag.find('iframe', src=re.compile(r"youtube|vimeo"))))
        if not f:
            return None
        fields = [inp.get('name') for inp in f.find_all('input') if inp.get('name')]
        return {"html": str(f), "fields": fields}
