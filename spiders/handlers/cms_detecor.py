from .base_handler import BaseHandler
from bs4 import BeautifulSoup
import re

class CMSDetector(BaseHandler):
    def name(self) -> str:
        return "cms"

    def extract(self, html: str) -> dict:
        # Возвращает словарь вида {"cms": <имя>}
        # Возможные значения: wordpress, bitrix, tilda, html5, unknown
        try:
            soup = BeautifulSoup(html, "html.parser")
            lower_html = html.lower()

            if meta := soup.find("meta", attrs={"name": re.compile(r"generator", re.I)}):
                content = meta.get("content", "").lower()
                for cms in ["wordpress", "bitrix", "tilda"]:
                    if cms in content:
                        return {"cms": cms}

            cms_checks = {
                "wordpress": [
                    lambda: soup.find(class_=re.compile(r"wp-header|site-header", re.I)),
                    lambda: any(re.search(p, lower_html) for p in [
                        r"/wp-content/",
                        r"/wp-includes",
                        r"wp-json",
                        r"/wp-login\.php",
                        r"/wp-admin",
                        r"/readme\.html"
                    ])
                ],
                "bitrix": [
                    lambda: any(re.search(p, lower_html) for p in [
                        r"/bitrix/",
                        r"bx_",
                        r"/bitrix/admin/"
                    ]),
                    lambda: any(
                        "x-bitrix" in tag.attrs.get("data-signed", "")
                        for tag in soup.find_all(attrs={"data-signed": True})
                    )
                ],
                "tilda": [
                    lambda: soup.find(class_=re.compile(r"t-\d+header|tilda", re.I)),
                    lambda: any(re.search(p, lower_html) for p in [
                        r"tilda\.cc",
                        r"static\.tildacdn\.info",
                        r"static\.tildacdn\.com"
                    ])
                ],
                "html5": [
                    lambda: (soup.find("header") or soup.find("footer"))
                            and not any(re.search(p, lower_html) for p in [
                                r"wp-",
                                r"bitrix",
                                r"tilda"
                            ]),
                    lambda: re.search(r"<!doctype html>", lower_html)
                ]
            }

            for cms, checks in cms_checks.items():
                if any(check() for check in checks):
                    return {"cms": cms}

            return {"cms": "unknown"}

        except Exception as e:
            self.logger.error(f"CMS detection error: {str(e)}")
            return {"cms": "unknown"}


