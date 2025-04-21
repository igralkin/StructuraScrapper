from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class BlockCalendar(BaseHandler):
    def name(self) -> str:
        return "block_calendar"

    def find_all(self, soup):
        return soup.select(".calendar, .date-picker, .schedule")

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        cal = soup.select_one(".calendar, .date-picker, .schedule")
        if not cal:
            return None
        days = [d.get_text(strip=True) for d in cal.select(".day")]
        return {"html": str(cal), "days": days}
