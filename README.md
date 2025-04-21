## 🕷 Structura Crawler

Асинхронный краулер на базе Scrapy для обхода сайтов и сбора HTML-страниц в рамках одного домена. Поддерживает ограничение по глубине, количеству страниц, фильтрацию расширений и экспорт в JSON.

---

### 🚀 Установка

```bash
git clone https://github.com/igralkin/StructuraScrapper.git
cd StructuraScrapper
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
│   ├── __init__.py
│   ├── detector.py
│   └── signatures.py
│
├── block_parser/              # Модуль парсинга header/footer
│   ├── __init__.py
│   ├── parser.py              # parse_blocks(html, cms, url)
│   ├── utils.py               # Логирование и утилиты
│   └── parsers/
│       ├── __init__.py
│       ├── base.py            # Общие методы поиска
│       ├── wordpress.py
│       ├── tilda.py
│       ├── bitrix.py
│       ├── html5.py
│       └── drupal.py
│
├── tests/                     # Юнит-тесты парсеров
│   ├── test_wordpress.py
│   ├── test_tilda.py
│   ├── test_bitrix.py
│   ├── test_drupal.py
│   └── test_html5.py
│
├── main.py
├── spiders/
│   └── base_spider.py
├── settings.py
├── requirements.txt
├── Dockerfile
├── .gitignore
└── output/
```
---

### 🔌 Интеграция CMS-детектора

Модуль `cms_detector` автоматически определяет CMS по HTML-коду страницы. 

Он уже встроен в `base_spider.py` и по умолчанию определяет CMS **только на первых 5 HTML-страницах** для повышения производительности.

**Формат результата в `output/data.json`:**
```json
{
  "url": "https://example.com",
  "depth": 0,
  "cms": "wordpress"
}
```

Вы можете изменить количество анализируемых страниц, отредактировав параметр `self.pages_crawled <= 5` в `BaseSpider.parse()`.

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

### 🧱 Парсинг блоков (Header/Footer Parser)

Модуль `block_parser` автоматически извлекает структурные блоки страницы (`<header>` и `<footer>`) на основе HTML-кода и типа CMS.

#### 📥 Входные параметры:
- HTML страницы (`str`)
- Название CMS (`str`): `wordpress`, `tilda`, `bitrix`, `html5`, `drupal`
- (опц.) URL страницы — для логирования

#### 📤 Формат результата:
```json
{
  "cms": "wordpress",
  "blocks": {
    "header": {
      "found": true,
      "content": "<header>...</header>",
      "strategy": "css:header"
    },
    "footer": {
      "found": true,
      "content": "<footer>...</footer>",
      "strategy": "id:colophon"
    }
  }
}
```

#### 🔍 Поддерживаемые CMS:
- **WordPress** — `site-header`, `masthead`, `site-footer`, теги `<header>` / `<footer>`
- **Tilda** — `t*-rec` с `t*-header`, `t*-footer` (ID: `rec123`)
- **Bitrix** — классы `bx-layout`, `adm-footer`, `bx-header`
- **HTML5** — теги `<header>`, `<footer>`
- **Drupal** — классы `region-header`, `region-footer`, `block-system-branding`, ID `branding`, `footer`

#### 🧪 Тесты:
Модуль покрыт юнит-тестами (`tests/`):
```bash
python -m unittest discover -s tests
```
#### 🔌 Интеграция в краулер:
Модуль встроен в `base_spider.py` и вызывается после определения CMS:
```python
from block_parser.parser import parse_blocks
blocks = parse_blocks(html, cms, url=response.url)
item['blocks'] = blocks
```

#### 📝 Логирование:
Логируются найденные блоки, стратегии и URL:
```
[https://example.com] HEADER — found: True, strategy: css:header
```
