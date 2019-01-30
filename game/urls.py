from django.urls import path
from . import views


app_name = 'game'

urlpatterns = [
    path('', views.WelcomeView.as_view(), name='amadventure'),
    path('main/', views.MainView.as_view(), name='main'),
    path('create_hero/', views.create_hero, name='create_hero'),
    path('hero_upgrade/', views.HeroUpgradeView.as_view(), name='hero_upgrade'),
    
]
