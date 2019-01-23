from django.shortcuts import redirect, reverse
from .models import Hero


def hero_created_require(function):
    def wrapper(request, *args, **kwargs):
        if not Hero.objects.filter(owner=request.user):
            return redirect(reverse('game:hero_create'))
        return function(request, *args, **kwargs)
    return wrapper
