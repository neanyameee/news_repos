from django import forms
from .models import NEWS_CATEGORIES, LANGUAGES, THEMES


class NewsPreferencesForm(forms.Form):
    categories = forms.MultipleChoiceField(
        choices=[(cat['id'], cat['name']) for cat in NEWS_CATEGORIES],
        widget=forms.CheckboxSelectMultiple,
        label='Категории новостей',
        required=False
    )


class NewsSettingsForm(forms.Form):
    language = forms.ChoiceField(
        choices=LANGUAGES,
        label='Язык интерфейса',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    theme = forms.ChoiceField(
        choices=THEMES,
        label='Тема оформления',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    email_notifications = forms.BooleanField(
        required=False,
        label='Получать уведомления на email'
    )

    email = forms.EmailField(
        required=False,
        label='Email для уведомлений',
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'your@email.com'})
    )