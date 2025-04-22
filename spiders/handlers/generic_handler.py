import yaml
from bs4 import BeautifulSoup
from .base_handler import BaseHandler

def load_blocks_config(path: str = 'spiders/handlers/blocks.yml') -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

class GenericHandler(BaseHandler):
    def __init__(self, block_type: str, config: dict):
        self.block_type = block_type
        self.cfg = config
        self.selectors = config.get('selectors', []) or []
        self.item_selector = config.get('item_selector', None)
        self.fields = config.get('fields', {})

    def name(self) -> str:
        return f"block_{self.block_type}"

    def extract(self, soup):
        results = []
        for sel in self.selectors:
            containers = soup.select(sel)
            for container in containers:
                items = container.select(self.item_selector) if self.item_selector else [container]
                for elem in items:
                    data = {'html': str(elem)}
                    for field, expr in self.fields.items():
                        if expr == 'self':
                            data[field] = elem.get_text(strip=True)
                            continue
                        css, *attr = expr.split('@')
                        el = elem.select_one(css)
                        if not el:
                            data[field] = None
                        else:
                            if attr:
                                data[field] = el.get(attr[0])
                            else:
                                data[field] = el.get_text(strip=True)
                    results.append(data)
        return results if results else None
