# 📦 CMS Detector Module

Модуль для автоматического определения CMS (Content Management System) на сайте по URL или HTML-коду. Поддерживает работу как в автономном режиме, так и в составе Scrapy-проекта.

---

## 🚀 Возможности

- Поддержка популярных CMS: WordPress, Tilda, Bitrix, Joomla, Drupal, HTML5 (fallback)
- Работа как по URL (с загрузкой страницы), так и напрямую по HTML-коду
- Подходит для встраивания в пайплайн Scrapy
- Устойчив к ошибкам сети

---

## 🧩 Структура модуля

```
cms_detector/
├── __init__.py
├── detector.py        # Основная логика определения CMS
└── signatures.py      # Сигнатуры и паттерны для каждой CMS
```

---

## 🧠 Как это работает

Модуль определяет CMS на основе:
- Мета-тега `<meta name="generator">`
- Ключевых слов в HTML (например, `wp-content` для WordPress)
- Характерных URL-структур (например, `/wp-login.php`)

---

## 🛠 Использование

### 1. По URL (с загрузкой страницы)

```python
from cms_detector.detector import detect_cms_by_url

cms = detect_cms_by_url("https://example.com")
print(cms)  # "wordpress" / "tilda" / ...
```

### 2. По HTML-коду

```python
from cms_detector.detector import detect_cms_by_html

with open("example.html") as f:
    html = f.read()

cms = detect_cms_by_html(html, url="https://example.com")
print(cms)
```

---

## 🔌 Интеграция с Scrapy

В пауке (`spiders/base_spider.py`):

```python
from cms_detector.detector import detect_cms_by_html

...

if self.pages_crawled <= 5:
    cms = detect_cms_by_html(response.text, response.url)
    self.logger.info(f"[CMS] {response.url} -> {cms}")
else:
    cms = None

yield {
    "url": response.url,
    "cms": cms,
    ...
}
```

---

## 📌 Зависимости

- Python 3.7+
- requests
- beautifulsoup4

Установка:
```bash
pip install requests beautifulsoup4
```

---

## ✅ Лицензия

MIT License