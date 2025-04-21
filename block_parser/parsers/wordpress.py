from bs4 import BeautifulSoup
from .base import find_by_tag, find_by_id_or_class, combine_strategies


def parse(soup: BeautifulSoup) -> dict:
    header = combine_strategies(
        find_by_tag(soup, "header"),
        find_by_id_or_class(soup, ["site-header", "masthead"], ["main-header", "navbar"])
    )

    footer = combine_strategies(
        find_by_tag(soup, "footer"),
        find_by_id_or_class(soup, ["colophon"], ["site-footer"])
    )

    return {
        "header": header,
        "footer": footer
    }
