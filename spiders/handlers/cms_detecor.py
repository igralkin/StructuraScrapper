from .base_handler import BaseHandler
from bs4 import BeautifulSoup
import re

class CMSDetector(BaseHandler):
    def name(self) -> str:
        return "cms"

    def extract(self, html: str) -> dict:
        # Возвращает словарь вида {"cms": <имя>}
        # Возможные значения: wordpress, bitrix, tilda, html5, unknown

        lower_html = html.lower()

        try:
            soup = BeautifulSoup(html, "html.parser")
            meta = soup.find("meta", attrs={"name": "generator"})
            
            if meta and meta.get("content"):
                gen = meta["content"].lower()
                if "wordpress" in gen:
                    return {"cms": "wordpress"}
                if "bitrix" in gen:
                    return {"cms": "bitrix"}
                if "tilda" in gen:
                    return {"cms": "tilda"}
        except Exception:
            pass
            #return {"cms": "unknown"}

        if (
            re.search(r"/wp-content/", lower_html)
            or re.search(r"/wp-login\.php", lower_html)
            or re.search(r"/wp-admin", lower_html)
            or re.search(r"/readme\.html", lower_html)
        ):
            return {"cms": "wordpress"}

        if re.search(r"/bitrix/", lower_html) or re.search(r"/bitrix/admin/", lower_html):
            return {"cms": "bitrix"}

        if "tilda.cc" in lower_html or "static.tildacdn" in lower_html:
            return {"cms": "tilda"}

        if re.search(r"<!doctype html>", lower_html):
            return {"cms": "html5"}

        return {"cms": "unknown"}


