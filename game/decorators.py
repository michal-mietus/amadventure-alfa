from django.shortcuts import redirect, reverse, get_object_or_404
from .models.hero import Hero


def hero_created_require(function):
    def wrapper(request, *args, **kwargs):
        if not Hero.objects.filter(user=request.user):
            return redirect(reverse('game:create_hero'))
        return function(request, *args, **kwargs)
    return wrapper


def logged_user_redirect_to_main_view(function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('game:main'))
        return function(request, *args, **kwargs)
    return wrapper
