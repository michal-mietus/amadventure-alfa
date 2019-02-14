from django.urls import path
from . import views


app_name = 'game'

urlpatterns = [
    path('', views.WelcomeView.as_view(), name='main'),
    path('hero/create/', views.CreateHeroView.as_view(), name='create_hero'),
    path('hero/upgrade/', views.UpgradeHeroView.as_view(), name='upgrade_hero'),
    path('hero/list/', views.HeroList.as_view(), name='hero_list'),
    path('hero/owned/', views.HeroOwned.as_view(), name='hero_owned'),
    path('hero/<int:pk>/', views.HeroDetail.as_view(), name='hero_detail'),
    path('hero/fight/<int:defender_pk>/', views.FightView.as_view(), name='hero_fight'),
    path('hero/delete/<int:pk>/', views.HeroDeleteView.as_view(), name='hero_delete'),
]
