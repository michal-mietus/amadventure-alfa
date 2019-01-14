from django.urls import path
from . import views


urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('create_hero/', views.CreateHeroView.as_view(), name='create_hero'),
]