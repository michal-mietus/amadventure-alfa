from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'usersystem'

urlpatterns = [
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('sign_in/', views.SignInView.as_view(), name='sign_in'),
    path('sign_out/', auth_views.LogoutView.as_view(), name='sign_out'),
]
