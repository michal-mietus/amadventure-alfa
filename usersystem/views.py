from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic.edit import FormView
from django.shortcuts import reverse
from django.utils.decorators import method_decorator
from .decorators import deny_logged_user_access


@method_decorator(deny_logged_user_access, name='dispatch')
class SignUpView(FormView):
    template_name = 'usersystem/sign_up.html'
    form_class = UserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('game:main')


@method_decorator(deny_logged_user_access, name='dispatch')
class SignInView(FormView):
    template_name = 'usersystem/sign_in.html'
    form_class = AuthenticationForm

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(self.request, user)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('game:main')
