from django.db import models


class NewsCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


# Данные в коде (как требуется в задании)
NEWS_CATEGORIES = [
    {'id': 1, 'name': 'Политика', 'description': 'Политические новости'},
    {'id': 2, 'name': 'Экономика', 'description': 'Экономические новости'},
    {'id': 3, 'name': 'Технологии', 'description': 'Технологические новости'},
    {'id': 4, 'name': 'Спорт', 'description': 'Спортивные новости'},
    {'id': 5, 'name': 'Культура', 'description': 'Культурные события'},
]

LANGUAGES = [
    ('ru', 'Русский'),
    ('en', 'English'),
    ('es', 'Español'),
]

THEMES = [
    ('light', 'Светлая'),
    ('dark', 'Темная'),
    ('auto', 'Авто'),
]