from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import NewsPreferencesForm
from .models import NEWS_CATEGORIES, LANGUAGES, THEMES
import json
from datetime import datetime, timedelta


def index(request):
    # Получаем настройки из cookies
    preferences = get_user_preferences(request)

    # Фильтруем новости по выбранным категориям
    selected_categories = preferences.get('categories', [])
    news = get_news_by_categories(selected_categories)

    context = {
        'news': news,
        'preferences': preferences,
        'form': NewsPreferencesForm(initial=preferences),
    }

    response = render(request, 'news/index.html', context)

    # Сохраняем историю посещений
    save_visit_history(request, response)

    return response


def preferences(request):
    if request.method == 'POST':
        form = NewsPreferencesForm(request.POST)
        if form.is_valid():
            # Сохраняем настройки в cookies
            response = redirect('index')

            preferences_data = {
                'categories': form.cleaned_data['categories'],
                'language': form.cleaned_data['language'],
                'theme': form.cleaned_data['theme'],
                'email_notifications': form.cleaned_data['email_notifications'],
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

    return render(request, 'news/preferences.html', {'form': form})


def get_user_preferences(request):
    default_preferences = {
        'categories': ['1', '2'],
        'language': 'ru',
        'theme': 'light',
        'email_notifications': False,
    }

    preferences_cookie = request.COOKIES.get('news_preferences')
    if preferences_cookie:
        try:
            user_preferences = json.loads(preferences_cookie)
            return {**default_preferences, **user_preferences}
        except json.JSONDecodeError:
            pass

    return default_preferences


def get_news_by_categories(category_ids):
    # Моковые данные новостей
    all_news = [
        {'id': 1, 'title': 'Важные политические изменения', 'category': '1', 'content': 'Описание новости...',
         'date': '2024-01-15'},
        {'id': 2, 'title': 'Экономический рост', 'category': '2', 'content': 'Описание новости...',
         'date': '2024-01-14'},
        {'id': 3, 'title': 'Новые технологии', 'category': '3', 'content': 'Описание новости...', 'date': '2024-01-13'},
        {'id': 4, 'title': 'Спортивные достижения', 'category': '4', 'content': 'Описание новости...',
         'date': '2024-01-12'},
        {'id': 5, 'title': 'Культурные события', 'category': '5', 'content': 'Описание новости...',
         'date': '2024-01-11'},
    ]

    if not category_ids:
        return all_news

    return [news for news in all_news if news['category'] in category_ids]


def save_visit_history(request, response):
    visit_history = request.COOKIES.get('visit_history', '[]')

    try:
        history = json.loads(visit_history)
    except json.JSONDecodeError:
        history = []

    # Добавляем текущее посещение
    current_visit = {
        'page': 'Главная',
        'timestamp': datetime.now().isoformat(),
        'url': request.path
    }

    history.append(current_visit)

    # Ограничиваем историю последними 5 посещениями
    history = history[-5:]

    response.set_cookie(
        'visit_history',
        json.dumps(history),
        max_age=30 * 24 * 60 * 60,  # 30 дней
        httponly=True
    )