from bs4 import BeautifulSoup
from .base import find_by_tag, find_by_id_or_class, combine_strategies


def parse(soup: BeautifulSoup) -> dict:
    header = combine_strategies(
        find_by_id_or_class(
            soup,
            ids=[],
            classes=["bx-header", "bx-layout"]
        ),
        find_by_tag(soup, "header")
    )

    footer = combine_strategies(
        find_by_id_or_class(
            soup,
            ids=[],
            classes=["bx-footer", "adm-footer", "bx-layout"]
        ),
        find_by_tag(soup, "footer")
    )

    return {
        "header": header,
        "footer": footer
    }