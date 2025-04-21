from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class BlockVideo(BaseHandler):
    def name(self) -> str:
        return "block_video"

    def find_all(self, soup):
        return soup.select("iframe[src*=youtube], video, .video-container")

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        vid = soup.find("iframe", src=re.compile(r"(youtube|vimeo)")) or soup.find("video")
        if not vid:
            return None
        src = vid.get("src") or vid.find("source")["src"]
        return {"html": str(vid), "src": src}
