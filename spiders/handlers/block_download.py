from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class BlockDownload(BaseHandler):
    def name(self) -> str:
        return "block_download"

    def find_all(self, soup):
        return soup.select("a[href$='.pdf'], .download-link, .file-download")

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        a = soup.select_one("a[href$='.pdf'], .download-link, .file-download")
        if not a:
            return None
        return {"html": str(a), "file": a["href"], "text": a.get_text(strip=True)}
