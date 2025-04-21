from .base_handler import BaseHandler
from bs4 import BeautifulSoup


class BlockTable(BaseHandler):
    def name(self) -> str:
        return "block_table"

    def extract(self, html: str) -> dict | None:
        # Блок с таблицей
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table")
        if not table:
            return None
        headers = [th.get_text(strip=True) for th in table.select("thead th")]
        rows = []
        for tr in table.select("tbody tr"):
            cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
            rows.append(cells)
        return {"html": str(table), "headers": headers, "rows": rows}

    def find_all(self, soup):
        return soup.select("table")