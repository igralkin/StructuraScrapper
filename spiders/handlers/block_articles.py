from .base_handler import BaseHandler
from bs4 import BeautifulSoup
import re

class BlockArticles(BaseHandler):
    #Статьи
    def name(self) -> str:
        return "block_articles"

    def find_all(self, soup):
        return soup.select(".articles, .blog-list, .news-list")

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        wrap = soup.select_one(".articles, .blog-list, .news-list")
        if not wrap:
            return None
        posts = []
        for post in wrap.select(".article, .post, li"):
            title = post.find(re.compile(r"^h[1-6]$"))
            summary = post.find("p")
            link = post.find("a", href=True)
            posts.append({"title": title.get_text(strip=True) if title else None, "summary": summary.get_text(strip=True) if summary else None, "url": link['href'] if link else None})
        return {"html": str(wrap), "posts": posts}