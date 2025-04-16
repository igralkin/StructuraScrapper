# main.py
import argparse
import os
from urllib.parse import urlparse
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.base_spider import BaseSpider


def main():
    parser = argparse.ArgumentParser(description="Simple website crawler using Scrapy")
    parser.add_argument("start_url", help="Starting URL for crawling")
    parser.add_argument("--max-pages", type=int, default=1000, help="Maximum number of pages to crawl")
    parser.add_argument("--depth", type=int, default=5, help="Maximum crawl depth")
    parser.add_argument("--save-html", action="store_true", help="Save HTML content in results")
    parser.add_argument("--output", type=str, default=None, help="Path to JSON output file")
    args = parser.parse_args()

    # Название сайта для путей
    parsed = urlparse(args.start_url)
    site_name = parsed.netloc.replace(".", "_")

    # По умолчанию сохраняем JSON в output/
    output_path = args.output or f"output/{site_name}_data.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    settings = get_project_settings()
    settings.set("FEEDS", {
        output_path: {
            'format': 'json',
            'encoding': 'utf8',
            'indent': 2,
        }
    })

    process = CrawlerProcess(settings)
    process.crawl(
        BaseSpider,
        start_url=args.start_url,
        max_pages=args.max_pages,
        depth=args.depth,
        save_html=args.save_html,
        site_name=site_name,
    )
    process.start()


if __name__ == "__main__":
    main()
