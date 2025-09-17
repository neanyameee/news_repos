from django import forms
from .models import NEWS_CATEGORIES, LANGUAGES, THEMES


class NewsPreferencesForm(forms.Form):
    categories = forms.MultipleChoiceField(
        choices=[(cat['id'], cat['name']) for cat in NEWS_CATEGORIES],
        widget=forms.CheckboxSelectMultiple,
        label='Категории новостей'
    )

    language = forms.ChoiceField(
        choices=LANGUAGES,
        label='Язык интерфейса'
    )

    theme = forms.ChoiceField(
        choices=THEMES,
        label='Тема оформления'
    )

    email_notifications = forms.BooleanField(
        required=False,
        label='Email уведомления'
    )