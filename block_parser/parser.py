"""
Главная точка входа для парсинга структурных блоков страниц (header, footer).
В зависимости от CMS маршрутизирует запрос к нужному подмодулю.
"""
from bs4 import BeautifulSoup
from .parsers import wordpress, tilda, bitrix, html5, drupal
from . import utils

# Сопоставление CMS → соответствующий парсер
CMS_PARSERS = {
    "wordpress": wordpress.parse,
    "drupal": drupal.parse,
    "tilda": tilda.parse,
    "bitrix": bitrix.parse,
    "html5": html5.parse
}


def parse_blocks(html: str, cms: str, url: str = None) -> dict:
    """
    Извлекает блоки header и footer из HTML-кода страницы в зависимости от CMS.

    :param html: HTML-документ страницы
    :param cms: название CMS (wordpress, tilda, bitrix, html5, drupal)
    :param url: URL страницы (опционально, для логирования)
    :return: словарь с извлечёнными блоками и стратегией поиска
    """
    cms = cms.lower()
    parser_func = CMS_PARSERS.get(cms, html5.parse)

    soup = BeautifulSoup(html, "html.parser")
    result = parser_func(soup)

    # Логируем найденные блоки
    if url:
        for block in ["header", "footer"]:
            utils.log_block_result(url, block, result.get(block, {}))

    return {
        # "cms": cms,
        "blocks": result
    }
