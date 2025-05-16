# base_spider.py
import scrapy
from urllib.parse import urlparse, urljoin
from block_parser.parser import parse_blocks
import os
import re
from cms_detector.detector import detect_cms_by_html


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

    def __init__(self, start_url, max_pages=1000, max_depth=5, save_html=False, site_name="site"):
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
        self.allowed_domain = urlparse(start_url).netloc
        self.site_name = site_name.replace(".", "_")

        self.max_pages = int(max_pages)
        self.max_depth = int(max_depth)
        self.save_html = save_html

        self.pages_crawled = 0
        self.visited_urls = set()
        self.output_dir = os.path.join("raw", self.site_name)

        # Подготовка папки с HTML (если включено сохранение)
        if self.save_html:
            os.makedirs(self.output_dir, exist_ok=True)
            # Очистка предыдущих HTML-файлов
            for fname in os.listdir(self.output_dir):
                fpath = os.path.join(self.output_dir, fname)
                if os.path.isfile(fpath):
                    os.remove(fpath)

        # Подготовка пути к лог-файлу ссылок и его очистка
        self.link_log_path = os.path.join("output", f"{self.site_name}_links.txt")
        os.makedirs("output", exist_ok=True)
        with open(self.link_log_path, "w", encoding="utf-8") as f:
            f.write("")  # очистка содержимого

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = cls(
            start_url=kwargs.get("start_url"),
            max_pages=kwargs.get("max_pages", 1000),
            max_depth=kwargs.get("max_depth", 5),
            save_html=kwargs.get("save_html", False),
            site_name=kwargs.get("site_name", "site")
        )
        spider.crawler = crawler
        spider.skip_extensions = crawler.settings.getlist("SKIP_EXTENSIONS") or []
        return spider

    def parse(self, response):
        """
        Обрабатывает страницу:
        - сохраняет HTML (если включено),
        - сохраняет ссылку и причину, если она пропущена,
        - извлекает новые внутренние ссылки.
        - определяет CMS (только на первых 5 страницах).
        """
        if self.pages_crawled >= self.max_pages:
            return iter([])

        content_type = response.headers.get("Content-Type", b"").decode("utf-8")
        is_text_html = "text/html" in content_type

        if not is_text_html:
            self.logger.debug(f"[SKIP] Non-HTML content at {response.url} (Content-Type: {content_type})")
            return iter([])

        self.pages_crawled += 1
        url = response.url
        self.visited_urls.add(url)

        # CMS определяем только на первых 5 страницах
        if self.pages_crawled <= 5:
            cms = detect_cms_by_html(response.text, url)
            self.logger.info(f"[CMS] {url} -> {cms}")
        else:
            cms = None

        # Парсинг header/footer блоков с защитой от ошибок
        try:
            blocks = parse_blocks(response.text, cms or "html5", url)
        except Exception as e:
            self.logger.warning(f"[PARSE ERROR] Failed to parse blocks at {url}: {e}")
            blocks = {}

        # Сохранение HTML
        if self.save_html:
            filename = self._safe_filename(url)
            filepath = os.path.join(self.output_dir, f"{filename}.html")
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(response.text)

        # Сохранение результата
        yield {
            "url": url,
            "depth": response.meta.get("depth", 0),
            "cms": cms,
            "blocks": blocks
        }

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

    def _safe_filename(self, url):
        """Преобразует URL в безопасное имя файла"""
        parsed = urlparse(url)
        path = parsed.path.strip("/").replace("/", "_") or "index"
        return re.sub(r"[^\w\-_.]", "_", path)

    def _should_skip_url(self, url):
        """Проверяет, нужно ли исключить URL по расширению"""
        return any(url.lower().endswith(ext) for ext in self.skip_extensions)
