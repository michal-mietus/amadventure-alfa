from django.urls import path
from . import views


app_name = 'game'

urlpatterns = [
    path('', views.WelcomeView.as_view(), name='amadventure'),
    path('main/', views.MainView.as_view(), name='main'),
    path('hero_create/', views.HeroCreateView.as_view(), name='hero_create'),
    path('hero_upgrade/', views.HeroUpgradeView.as_view(), name='hero_upgrade'),
    
]
