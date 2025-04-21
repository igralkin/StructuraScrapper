from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class BlockVideoText(BaseHandler):
    #Видео с текст
    def name(self) -> str:
        return "block_video_text"

    def find_all(self, soup):
        return soup.select(".video-text, .text-video, .block-video-text")

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        cont = soup.select_one(".video-text, .text-video, .block-video-text")
        if not cont:
            return None
        vid = cont.find(lambda tag: tag.name=='iframe' or tag.name=='video')
        txt = cont.get_text(strip=True)
        return {"html": str(cont), "text": txt, "video_src": vid.get('src') if vid else None}
