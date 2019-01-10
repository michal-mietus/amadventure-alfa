from django.contrib import admin
from django.urls import path, include
from game.urls import urlpatterns as game_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('game/', include(game_urls))
]
