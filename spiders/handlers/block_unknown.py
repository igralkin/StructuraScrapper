from .base_handler import BaseHandler

class BlockUnknown(BaseHandler):
    def name(self) -> str:
        return "block_unknown"

    def find_all(self, soup):
        return []

    def extract(self, html: str) -> dict | None:
        return None