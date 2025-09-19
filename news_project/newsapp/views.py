from django.shortcuts import render, redirect
from .forms import NewsPreferencesForm, NewsSettingsForm
from .models import NEWS_CATEGORIES
import json
from datetime import datetime


# Вспомогательные функции
def get_user_preferences(request):
    default_preferences = {
        'categories': ['1', '2'],
    }

    preferences_cookie = request.COOKIES.get('news_preferences')
    if preferences_cookie:
        try:
            user_preferences = json.loads(preferences_cookie)
            return {**default_preferences, **user_preferences}
        except json.JSONDecodeError:
            pass

    return default_preferences


def get_user_settings(request):
    default_settings = {
        'language': 'ru',
        'theme': 'light',
        'email_notifications': False,
        'email': '',
    }

    settings_cookie = request.COOKIES.get('news_settings')
    if settings_cookie:
        try:
            user_settings = json.loads(settings_cookie)
            return {**default_settings, **user_settings}
        except json.JSONDecodeError:
            pass

    return default_settings


def get_news_by_categories(category_ids):
    all_news = [
        {'id': 1, 'title': 'Важные политические изменения', 'category': '1',
         'content': 'Сегодня произошли значительные изменения в политической системе страны...', 'date': '2025-09-19'},
        {'id': 2, 'title': 'Экономический рост', 'category': '2',
         'content': 'Экономика показывает стабильный рост в последнем квартале...', 'date': '2025-09-18'},
        {'id': 3, 'title': 'Новые технологии', 'category': '3',
         'content': 'Ученые представили революционную технологию в области искусственного интеллекта...',
         'date': '2025-09-17'},
        {'id': 4, 'title': 'Спортивные достижения', 'category': '4',
         'content': 'Национальная сборная установила новый рекорд на международных соревнованиях...',
         'date': '2025-09-16'},
        {'id': 5, 'title': 'Культурные события', 'category': '5',
         'content': 'В столице открылась масштабная выставка современного искусства...', 'date': '2025-09-15'},
    ]

    if not category_ids:
        return all_news

    return [news for news in all_news if news['category'] in category_ids]


# Основные представления
def index(request):
    preferences = get_user_preferences(request)
    settings = get_user_settings(request)

    selected_categories = preferences.get('categories', [])
    news = get_news_by_categories(selected_categories)

    context = {
        'news': news,
        'preferences': preferences,
        'settings': settings,
    }

    return render(request, 'newsapp/index.html', context)


def preferences_view(request):
    if request.method == 'POST':
        form = NewsPreferencesForm(request.POST)
        if form.is_valid():
            response = redirect('index')

            preferences_data = {
                'categories': form.cleaned_data['categories'],
                'updated_at': datetime.now().isoformat(),
            }

            response.set_cookie(
                'news_preferences',
                json.dumps(preferences_data),
                max_age=365 * 24 * 60 * 60,
                httponly=True
            )

            return response
    else:
        preferences = get_user_preferences(request)
        form = NewsPreferencesForm(initial=preferences)

    return render(request, 'newsapp/preferences.html', {'form': form})


def settings_view(request):
    if request.method == 'POST':
        form = NewsSettingsForm(request.POST)
        if form.is_valid():
            response = redirect('index')

            settings_data = {
                'language': form.cleaned_data['language'],
                'theme': form.cleaned_data['theme'],
                'email_notifications': form.cleaned_data['email_notifications'],
                'email': form.cleaned_data['email'],
                'updated_at': datetime.now().isoformat(),
            }

            response.set_cookie(
                'news_settings',
                json.dumps(settings_data),
                max_age=365 * 24 * 60 * 60,
                httponly=True
            )

            return response
    else:
        settings = get_user_settings(request)
        form = NewsSettingsForm(initial=settings)

    return render(request, 'newsapp/settings.html', {'form': form})