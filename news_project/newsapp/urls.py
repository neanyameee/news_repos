from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('preferences/', views.preferences_view, name='preferences'),
    path('settings/', views.settings_view, name='settings'),
]