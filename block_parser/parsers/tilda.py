# Обновлённая функция поиска блоков Tilda
# Ищет <div> с классами вида t123-header, t456-footer внутри t*-rec


from bs4 import BeautifulSoup
from .base import combine_strategies


HEADER_CLASSES = ["t-header", "t*-header"]
FOOTER_CLASSES = ["t-footer", "t*-footer"]

# Улучшенная эвристика: ищет <div> с rec-классом и одновременным наличием *-header или *-footer


def find_tilda_block(soup: BeautifulSoup, suffix: str):
    candidates = soup.find_all("div", class_=lambda x: x and any("rec" in c for c in x))
    for el in candidates:
        cls = el.get("class", [])
        if any(c.endswith(suffix) for c in cls):
            match_cls = next((c for c in cls if c.endswith(suffix)), "")
            return (str(el), f"class:{match_cls}")
    return None


def parse(soup: BeautifulSoup) -> dict:
    header = combine_strategies(
        find_tilda_block(soup, "-header")
    )

    footer = combine_strategies(
        find_tilda_block(soup, "-footer")
    )

    return {
        "header": header,
        "footer": footer
    }
