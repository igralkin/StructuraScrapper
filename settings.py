# settings.py

BOT_NAME = 'crawler'

SPIDER_MODULES = ['spiders']
NEWSPIDER_MODULE = 'spiders'

ROBOTSTXT_OBEY = True
ROBOTSTXT_OBEY = False

LOG_LEVEL = 'INFO'

DEPTH_LIMIT = 5
CLOSESPIDER_PAGECOUNT = 1000

DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; StructuraCrawler/1.0)'
}

DOWNLOAD_DELAY = 0.25
CONCURRENT_REQUESTS = 16

# Файлы, которые не нужно качать
SKIP_EXTENSIONS = [
    ".pdf", ".svg", ".jpg", ".jpeg", ".png", ".zip", ".tar", ".gz", ".rar", ".mp4", ".mp3"
]
