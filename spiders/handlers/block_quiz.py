from .base_handler import BaseHandler
from bs4 import BeautifulSoup

class BlockQuiz(BaseHandler):
    #Квиз или опрос
    def name(self) -> str:
        return "block_quiz"

    def find_all(self, soup):
        return soup.select(".quiz, .survey, .poll")

    def extract(self, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")
        q = soup.select_one(".quiz, .survey, .poll")
        if not q: return None
        questions = [q_ for q_ in q.select(".question")]
        return {"html": str(q), "questions_count": len(questions)}