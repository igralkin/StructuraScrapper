from .base_handler import BaseHandler
from bs4 import BeautifulSoup
import re

class BlockAuth(BaseHandler):
    def name(self) -> str:
        return "block_auth"

    def find_all(self, soup):
        return soup.select("form[action*='login'], .login-form, .auth-block")

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        f = soup.find("form", action=re.compile(r"(login|auth)"))
        if not f:
            return None
        fields = [inp.get("name") for inp in f.find_all("input", {"name": True})]
        return {"html": str(f), "fields": fields}
