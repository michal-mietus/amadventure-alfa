from django.shortcuts import render, reverse, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import HeroCreateForm, HeroUpgradeForm
from .models import Hero
from .decorators import hero_created_require


@method_decorator(login_required, name='dispatch')
class MainView(TemplateView):
    template_name = 'game/main.html'


@method_decorator(login_required, name='dispatch')
class HeroCreateView(FormView):
    template_name = 'game/create_hero.html'
    form_class = HeroCreateForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('game:main')


# why decorator works but overriding method and super() call doesnt
@method_decorator(hero_created_require, name='dispatch')
@method_decorator(login_required, name='dispatch')
class HeroUpgradeView(UpdateView):
    template_name = 'game/upgrade_hero.html'
    form_class = HeroUpgradeForm
    model = Hero

    def get_object(self, queryset=None):
        # TODO how get current hero (if we would have more than one to choose)?
        obj = Hero.objects.get(owner=self.request.user)
        return obj

    def get_initial(self):
        initial = super(HeroUpgradeView, self).get_initial()
        # TODO how get current hero (if we would have more than one to choose)?
        hero = Hero.objects.get(owner=self.request.user)
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
