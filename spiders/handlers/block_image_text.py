from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class BlockImageText(BaseHandler):
    def name(self) -> str:
        return "block_image_text"

    def extract(self, html: str) -> dict | None:
        # Поиск блока, в котором сначала изображение, затем текст
        soup = BeautifulSoup(html, "html.parser")
        containers = soup.select(".block-image-text, .img-text, div.image-text")
        results = []
        for cont in containers:
            items = [t for t in cont.find_all(["img", "p", "span"], recursive=False)]
            img = next((t for t in items if t.name=="img"), None)
            txt = next((t for t in items if t.name in ("p", "span")), None)
            if not img or not txt:
                continue
            if items.index(img) < items.index(txt):
                results.append({
                    "html": str(cont),
                    "image_src": img.get("src"),
                    "text": txt.get_text(strip=True)
                })
        if results:
            return {"blocks": results}
        return None

    def find_all(self, soup):
        return soup.select(".block-image-text, .img-text, div.image-text")