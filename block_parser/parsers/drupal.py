from bs4 import BeautifulSoup
from .base import find_by_tag, find_by_id_or_class, combine_strategies

# Drupal часто использует классы: region-header, region-footer, block-system-branding
# Также встречаются ID: header, footer, branding


def parse(soup: BeautifulSoup) -> dict:
    header = combine_strategies(
        find_by_id_or_class(
            soup,
            ids=["header", "branding"],
            classes=["region-header", "block-system-branding"]
        ),
        find_by_tag(soup, "header")
    )

    footer = combine_strategies(
        find_by_id_or_class(
            soup,
            ids=["footer"],
            classes=["region-footer"]
        ),
        find_by_tag(soup, "footer")
    )

    return {
        "header": header,
        "footer": footer
    }