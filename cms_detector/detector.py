# detector.py
"""
Модуль определения CMS по URL или HTML-коду.
"""

import requests
from bs4 import BeautifulSoup
from typing import Optional

from .signatures import CMS_SIGNATURES


def detect_cms_by_url(url: str) -> str:
    """
    Определяет CMS сайта по его URL.

    :param url: URL сайта
    :return: Название CMS (например, 'wordpress', 'joomla', 'html5')
    """
    try:
        response = requests.get(url, timeout=10)
        html = response.text
        return detect_cms_by_html(html, url=url)
    except requests.RequestException:
        return 'html5'


def detect_cms_by_html(html: str, url: Optional[str] = None) -> str:
    """
    Определяет CMS сайта по HTML-коду.

    :param html: HTML-контент страницы
    :param url: URL страницы (опционально, используется для формирования путей)
    :return: Название CMS
    """
    soup = BeautifulSoup(html, 'html.parser')

    # Проверка мета-тега generator
    meta_generator = soup.find('meta', attrs={'name': 'generator'})
    if meta_generator and meta_generator.get('content'):
        content = meta_generator['content']
        for cms, sig in CMS_SIGNATURES.items():
            if sig['meta_generator'].search(content):
                return cms

    # Проверка ключевых слов в HTML
    for cms, sig in CMS_SIGNATURES.items():
        if any(keyword in html for keyword in sig['keywords']):
            return cms

    # Проверка наличия специфичных путей (если указан URL)
    if url:
        for cms, sig in CMS_SIGNATURES.items():
            for path in sig['paths']:
                try:
                    path_url = url.rstrip('/') + path
                    path_response = requests.get(path_url, timeout=5)
                    if path_response.status_code == 200:
                        return cms
                except requests.RequestException:
                    continue

    return 'html5'


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m cms_detector.detector <url>")
    else:
        cms = detect_cms_by_url(sys.argv[1])
        print(f'CMS: {cms}')
