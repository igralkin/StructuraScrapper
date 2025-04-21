from bs4 import BeautifulSoup
from .base import find_by_tag, combine_strategies


def parse(soup: BeautifulSoup) -> dict:
    header = combine_strategies(
        find_by_tag(soup, "header")
    )

    footer = combine_strategies(
        find_by_tag(soup, "footer")
    )

    return {
        "header": header,
        "footer": footer
    }