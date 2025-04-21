from .base_handler import BaseHandler
from bs4 import BeautifulSoup


class BlockContacts(BaseHandler):
    def name(self) -> str:
        return "block_contacts"

    def extract(self, html: str) -> dict | None:
        # Контакты
        soup = BeautifulSoup(html, "html.parser")
        cont = soup.select_one(".contact, .contacts, .footer-contacts")
        if not cont:
            return None
        phones = [a.get_text(strip=True) for a in cont.select("a[href^=tel]")]
        mails = [a.get_text(strip=True) for a in cont.select("a[href^=mailto]")]
        socials = [a["href"] for a in cont.select("a[href^=http]") if "tel:" not in a["href"] and "mailto:" not in a["href"]]
        return {
            "html": str(cont),
            "phones": phones,
            "emails": mails,
            "socials": socials
        }

    def find_all(self, soup):
        return soup.select(".contact, .contacts, .footer-contacts")