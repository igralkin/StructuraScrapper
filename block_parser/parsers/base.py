from bs4 import BeautifulSoup
from typing import Optional, List, Tuple


def find_by_tag(soup: BeautifulSoup, tag: str) -> Optional[Tuple[str, str]]:
    el = soup.find(tag)
    if el:
        return (str(el), f"css:{tag}")
    return None


def find_by_id_or_class(soup: BeautifulSoup, ids: List[str], classes: List[str]) -> Optional[Tuple[str, str]]:
    for id_ in ids:
        el = soup.find(id=id_)
        if el:
            return (str(el), f"id:{id_}")
    for cls in classes:
        el = soup.find(class_=lambda x: x and cls in x)
        if el:
            return (str(el), f"class:{cls}")
    return None


def combine_strategies(*results) -> dict:
    if results:
        for r in results:
            if r:
                return {"found": True, "content": r[0], "strategy": r[1]}
    return {"found": False, "content": "", "strategy": ""}
