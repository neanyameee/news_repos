from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('preferences/', views.preferences, name='preferences'),
]