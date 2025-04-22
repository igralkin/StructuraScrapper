#base_handler
from abc import ABC, abstractmethod

class BaseHandler(ABC):
    @abstractmethod
    def name(self) -> str:
        #Возваращает уникальный ключ, под которым будут сохраняться данные хендлера в результате
        pass

    @abstractmethod
    def extract(self, html: str) -> dict | None:
        #Выполняет анализ HTML и возвращает словарь с результатами.
        #Если блок не найден или детектор не применим, возвращает None
        pass

    #@abstractmethod
    #def find_all(self, soup):
    #    pass