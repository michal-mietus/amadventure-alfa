from django.urls import path
from . import views


app_name = 'game'

urlpatterns = [
    path('', views.WelcomeView.as_view(), name='amadventure'),
    path('main/', views.MainView.as_view(), name='main'),
    path('create_hero/', views.CreateHeroView.as_view(), name='create_hero'),
    path('upgrade_hero/', views.UpgradeHeroView.as_view(), name='upgrade_hero'),
    path('hero/<int:pk>/', views.HeroDetail.as_view(), name='hero_detail'),
]
