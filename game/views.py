from django.shortcuts import render, reverse
from django.views.generic.edit import View, FormView
from .forms import HeroCreateForm, HeroUpgradeForm
from .models import Hero


class MainView(View):
    template_name = 'game/main.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class HeroCreateView(FormView):
    template_name = 'game/create_hero.html'
    form_class = HeroCreateForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('game:main')


class HeroUpgradeView(FormView):
    template_name = 'game/upgrade_hero.html'
    form_class = HeroUpgradeForm

    def get_initial(self):
        initial = super(HeroUpgradeView, self).get_initial()
        # TODO how get current hero (if we would have more than one to choose)?
        hero = Hero.objects.get(user=self.request.user)
        initial['strength'] = hero.strength
        initial['intelligence'] = hero.intelligence
        initial['agility'] = hero.agility
        initial['vitality'] = hero.vitality

        return initial

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('game:main')
