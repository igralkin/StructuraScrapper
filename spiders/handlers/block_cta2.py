from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class BlockCTA2(BaseHandler):
    #Призыв к действию
    def name(self) -> str:
        return "block_call_to_action"

    def find_all(self, soup):
        return soup.select(".cta, .call-to-action, .block-cta")

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        cont = soup.select_one(".cta, .call-to-action, .block-cta")
        if not cont:
            return None
        btn = cont.find("button") or cont.find("a", role="button")
        txt = cont.get_text(strip=True)
        return {"html": str(cont), "text": txt, "action": btn.get_text(strip=True) if btn else None}