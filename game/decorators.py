from django.shortcuts import redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from .models.hero import Hero


def hero_created_require(function):
    def wrapper(request, *args, **kwargs):
        if not Hero.objects.filter(user=request.user):
            return redirect(reverse('game:create_hero'))
        return function(request, *args, **kwargs)
    return wrapper


def deny_user_create_more_than_one_hero(function):
    def wrapper(request, *args, **kwargs):
        hero = Hero.objects.filter(user=request.user)
        if hero:
             # we assume that we will not allow user create more than 1 hero
             # anywhere else
            return redirect(reverse_lazy('game:main'))
        return function(request, *args, **kwargs)
    return wrapper