from django.shortcuts import render
from django.views.generic.edit import View, FormView
from .forms import HeroForm


class MainView(View):
    template_name = 'game/main.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class CreateHeroView(FormView):
    template_name = 'game/create_hero.html'
    form_class = HeroForm
    success_url = '/'

    def form_valid(self, form):
        return render(request, 'game/index.html')
