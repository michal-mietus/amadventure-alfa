from django.urls import path
from . import views


app_name = 'game'

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('create_hero/', views.CreateHeroView.as_view(), name='create_hero'),
]
