from .base_handler import BaseHandler
from bs4 import BeautifulSoup


class BlockTimeline(BaseHandler):
    def name(self) -> str:
        return "block_timeline"

    def extract(self, html: str) -> dict | None:
        # Таймлайн
        soup = BeautifulSoup(html, "html.parser")
        wrap = soup.select_one(".timeline, .timeline-container")
        if not wrap:
            return None
        events = []
        for ev in wrap.select(".timeline-item, .event"):
            date = ev.find(class_="date")
            desc = ev.find("p") or ev.get_text(strip=True)
            events.append({
                "html": str(ev),
                "date": date.get_text(strip=True) if date else None,
                "text": desc.get_text(strip=True) if hasattr(desc, "get_text") else desc
            })
        return {
            "html": str(wrap), "events": events}

    def find_all(self, soup):
        return soup.select(".timeline, .timeline-item, .history")