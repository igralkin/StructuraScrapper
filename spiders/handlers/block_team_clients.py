from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class BlockTeamClients(BaseHandler):
    def name(self) -> str:
        return "block_team_clients"

    def find_all(self, soup):
        return soup.select(".team, .our-team, .clients, .our-clients")

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        wrap = soup.select_one(".team, .our-team, .clients, .our-clients")
        if not wrap:
            return None
        people = [p.get_text(strip=True) for p in wrap.select(".member, .client-name")]
        return {"html": str(wrap), "names": people}
