# README.md

## 🕷 Structura Crawler

Асинхронный краулер на базе Scrapy для обхода сайтов и сбора HTML-страниц в рамках одного домена. Поддерживает ограничение по глубине, количеству страниц, фильтрацию расширений и экспорт в JSON.

---

### 🚀 Установка

```bash
git clone https://github.com/your-repo/structura-crawler.git
cd structura-crawler
pip install -r requirements.txt
```

---

### ▶️ Запуск

```bash
python main.py https://example.com \
  --max-pages 1000 \
  --depth 5 \
  --save-html \
  --output output/data.json
```

**Параметры:**
- `start_url` — стартовая страница
- `--max-pages` — максимум страниц (по умолчанию 1000)
- `--depth` — максимальная глубина (по умолчанию 5)
- `--save-html` — сохранять HTML каждой страницы в `output/`
- `--output` — путь к JSON-файлу с результатами

---

### 📁 Структура проекта
```
crawler/
├── cms_detector/              # Модуль определения CMS
│   ├── __init__.py            # Инициализация пакета
│   ├── detector.py            # Основная логика определения CMS по URL/HTML
│   └── signatures.py          # Сигнатуры для различных CMS
│
├── main.py                    # CLI-интерфейс
├── spiders/
│   └── base_spider.py         # Логика краулера
├── settings.py                # Настройки Scrapy
├── requirements.txt           # Зависимости
├── Dockerfile                 # Контейнеризация
├── .gitignore                 # Исключения
└── output/                    # Выходные данные (html, json)
```

---

### 🐳 Запуск через Docker

```bash
docker build -t structura-crawler .
docker run structura-crawler https://example.com --max-pages 200 --depth 3 --save-html
```

---

### ⚙️ Настройки (settings.py)
- `SKIP_EXTENSIONS` — расширения файлов, которые не скачиваются (например .pdf, .svg)
- `DEPTH_LIMIT`, `CLOSESPIDER_PAGECOUNT` — лимиты краулера

---

### ✅ Поддержка
- Внутренние ссылки (в рамках одного домена)
- Асинхронный обход
- Уважает robots.txt
- Фильтрация ссылок по расширениям
- Возможность масштабирования на большие сайты (1000+ страниц)

---

### 📌 Примеры сайтов для теста
- https://botcreators.ru
- https://structura.app
- https://automatisation.art
- https://mindbox.ru
- https://skillfactory.ru