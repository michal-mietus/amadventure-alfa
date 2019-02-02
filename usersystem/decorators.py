from django.http import HttpResponseRedirect
from django.shortcuts import reverse


def deny_logged_user_access(function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('game:main'))
        return function(request, *args, **kwargs)
    return wrapper
