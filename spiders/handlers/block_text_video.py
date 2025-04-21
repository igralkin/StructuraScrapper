from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class BlockTextVideo(BaseHandler):
    #Блок текст с видео
    def name(self) -> str:
        return "block_text_video"

    def find_all(self, soup):
        return soup.select(".text-video, .video-text, .block-text-video")

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        cont = soup.select_one(".text-video, .video-text, .block-text-video")
        if not cont:
            return None
        txt = cont.get_text(strip=True)
        vid = cont.find(lambda tag: tag.name=='iframe' or tag.name=='video')
        src = vid.get('src') if vid else None
        return {"html": str(cont), "text": txt, "video_src": src}