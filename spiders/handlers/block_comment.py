from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class BlockComment(BaseHandler):
    #Комментарий
    def name(self) -> str:
        return "block_comment"

    def find_all(self, soup):
        return soup.select(".comment, .comments-list, .discussion")

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        wrap = soup.select_one(".comment, .comments-list, .discussion")
        if not wrap:
            return None
        comments = [c.get_text(strip=True) for c in wrap.select(".comment-item, li")]
        return {"html": str(wrap), "comments": comments}
