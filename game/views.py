from django.shortcuts import render, reverse
from django.views.generic.edit import View, FormView
from .forms import HeroForm


class MainView(View):
    template_name = 'game/main.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class CreateHeroView(FormView):
    template_name = 'game/create_hero.html'
    form_class = HeroForm

    def get_success_url(self):
        return reverse('game:main')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)
