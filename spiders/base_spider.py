# base_spider.py
import scrapy
from urllib.parse import urlparse, urljoin
import os
import re
from bs4 import BeautifulSoup

from spiders.handlers.base_handler import BaseHandler
from spiders.handlers.generic_handler import GenericHandler, load_blocks_config
from spiders.handlers.cms_detecor import CMSDetector

class BaseSpider(scrapy.Spider):
    """
    Асинхронный краулер, обходящий только внутренние страницы сайта,
    с поддержкой ограничения по глубине, числу страниц и сохранением HTML.
    """
    name = 'base_spider'
    custom_settings = {
        'DEPTH_LIMIT': 5,
        'CLOSESPIDER_PAGECOUNT': 1000,
        'ROBOTSTXT_OBEY': False,
    }

    def __init__(self, start_url, max_pages=1000, max_depth=5, save_html=False, site_name="site", config_path: str = 'spiders/handlers/blocks.yml'):
        """
        Инициализация параметров краулера.

        :param start_url: URL для начала обхода
        :param max_pages: Максимальное количество страниц
        :param max_depth: Максимальная глубина обхода
        :param save_html: Флаг сохранения HTML-файлов
        :param site_name: Название сайта для логов и вывода
        """
        super().__init__()

        self.start_urls = [start_url]
        parsed = urlparse(start_url)
        self.allowed_domain = parsed.netloc
        self.site_name = site_name.replace(".", "_")

        self.max_pages = int(max_pages)
        self.max_depth = int(max_depth)
        self.save_html = save_html

        self.pages_crawled = 0
        self.visited_urls = set()

        #Путь для сохранения HTML
        self.output_dir = os.path.join("raw", self.site_name)

        self.cms_detector = CMSDetector()

        # Загрузка config
        self.blocks_cfg = load_blocks_config(config_path)
        self.block_handlers = [GenericHandler(bt, conf) for bt, conf in self.blocks_cfg.items()]

        # Подготовка пути к лог-файлу ссылок и его очистка
        self.link_log_path = os.path.join("output", f"{self.site_name}_links.txt")
        os.makedirs("output", exist_ok=True)
        with open(self.link_log_path, "w", encoding="utf-8") as f:
            f.write("")  # очистка содержимого

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        if not hasattr(spider.cms_detector, "extract"):
            raise RuntimeError("CMSDetector not initialized")

        crawler.settings.set('DEPTH_LIMIT', spider.max_depth)
        crawler.settings.set('CLOSESPIDER_PAGECOUNT', spider.max_pages)
        crawler.settings.set('DOWNLOAD_DELAY', crawler.settings.get('DOWNLOAD_DELAY', 0.25))
        spider.skip_extensions = crawler.settings.getlist("SKIP_EXTENSIONS")
        return spider

    def parse(self, response):

        """
        Обрабатывает страницу:
        - сохраняет HTML (если включено),
        - сохраняет ссылку и причину, если она пропущена,
        - извлекает новые внутренние ссылки.
        """
        if self.pages_crawled >= self.max_pages:
            return

        content_type = response.headers.get("Content-Type", b"").decode("utf-8")
        is_text_html = "text/html" in content_type

        self.pages_crawled += 1
        url = response.url
        self.visited_urls.add(url)

        # Сохранение HTML
        if self.save_html and is_text_html:
            filename = self._safe_filename(url)
            filepath = os.path.join(self.output_dir, f"{filename}.html")
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(response.text)

        result = {
            "url": url,
            "depth": response.meta.get("depth", 0)
        }

        if is_text_html:
            soup = BeautifulSoup(response.text, "lxml")


            cms_data = self.cms_detector.extract(soup)
            cms = cms_data.get("cms", "unknown")
            result["cms"] = cms

            # Debug
            self.logger.info(f"[DEBUG] Detected CMS: {cms}")
            self.logger.info(f"[DEBUG] Block handlers: {[h.name() for h in self.block_handlers]}")

            #Debug
            #for h in self.block_handlers:
            #   cnt = len(h.find_all(soup))
            #    self.logger.info(f"[DEBUG] handler {h.name()} found {cnt}")

            structure = []
            for handler in self.block_handlers:
                if handler.block_type == "cms":
                    continue
                blocks = handler.extract(soup)
                if not blocks:
                    continue
                for data in blocks:
                    block_html = data.pop("html", None)
                    entry = {"type": handler.name(), "html": block_html, **data}
                    structure.append(entry)
            result["structure"] = structure

            yield result

        # Подготовка пути к файлу ссылок
        link_log_path = os.path.join("output", f"{self.site_name}_links.txt")
        os.makedirs("output", exist_ok=True)

        links = response.css("a::attr(href)").getall()
        for href in links:
            abs_url = urljoin(response.url, href)
            domain = urlparse(abs_url).netloc
            skip_reason = None

            # Логируем в файл
            with open(link_log_path, "a", encoding="utf-8") as f:
                f.write(f"{response.url} -> {href}\n")

            # Проверка причин пропуска
            if abs_url in self.visited_urls:
                skip_reason = "already visited"
            elif domain != self.allowed_domain:
                skip_reason = "external domain"
            elif self._should_skip_url(abs_url):
                skip_reason = "disallowed extension"

            if skip_reason:
                self.logger.debug(f"[SKIP] {abs_url} ({skip_reason})")
                with open(link_log_path, "a", encoding="utf-8") as f:
                    f.write(f"[SKIP] {response.url} -> {href} ({skip_reason})\n")
                continue

            # Переход по ссылке
            yield response.follow(abs_url, callback=self.parse)


        # Прекращаем обработку, если это не HTML
        if not is_text_html:
            self.logger.debug(f"[SKIP] Non-HTML content at {response.url} (Content-Type: {content_type})")
            return

    def _safe_filename(self, url):
        """Преобразует URL в безопасное имя файла"""
        parsed = urlparse(url)
        path = parsed.path.strip("/").replace("/", "_") or "index"
        return re.sub(r"[^\w\-_.]", "_", path)


    def _should_skip_url(self, url):
        """Проверяет, нужно ли исключить URL по расширению"""
        return any(url.lower().endswith(ext) for ext in self.skip_extensions)
