"""
Сигнатуры и паттерны для определения различных CMS.
"""

import re

CMS_SIGNATURES = {
    'wordpress': {
        'meta_generator': re.compile(r'WordPress', re.I),
        'paths': ['/wp-login.php', '/wp-admin/'],
        'keywords': ['wp-content', 'wp-includes', 'wp-json', 'wp-']
    },
    'joomla': {
        'meta_generator': re.compile(r'Joomla', re.I),
        'paths': ['/administrator/'],
        'keywords': ['com_content', 'mod_login']
    },
    'drupal': {
        'meta_generator': re.compile(r'Drupal', re.I),
        'paths': ['/user/login'],
        'keywords': ['drupal-settings-json', 'sites/all', 'drupal.js']
    },
    'bitrix': {
        'meta_generator': re.compile(r'Bitrix', re.I),
        'paths': ['/bitrix/admin/', '/bitrix/templates/', '/bitrix/js/'],
        'keywords': ['bitrix', 'bx-core', 'bx-admin', 'adm-', 'bx-']
    },
    'tilda': {
        'meta_generator': re.compile(r'Tilda', re.I),
        'paths': [],
        'keywords': ['t[0-9]+-rec', 't[0-9]+-header', 't[0-9]+-footer',
                     'data-tilda-', 'tilda.cc', 'tildacdn.com']
    },
    'html5': {
        'meta_generator': re.compile(r'', re.I),
        'paths': [],
        'keywords': []  # Фолбэк, если ничего не найдено
    }
}
