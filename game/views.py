import math
from random import randrange
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.base import ContextMixin, View
from django.views.generic.edit import FormView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .decorators import hero_created_require, logged_user_redirect_to_main_view, deny_user_create_more_than_one_hero
from .forms import HeroForm, MainStatisticsForm
from .models.hero import Hero
from .models.item import Item
from .models.statistics import HeroMainStatistic, HeroDerivativeStatistic
from .statistic_properties import main_statistics, derivative_statistics


@method_decorator(logged_user_redirect_to_main_view, name='dispatch')
class WelcomeView(TemplateView):
    template_name = 'game/amadventure.html'


@method_decorator(login_required, name='dispatch')
class MainView(TemplateView):
    template_name = 'game/main.html'


@method_decorator(login_required, name='dispatch')
@method_decorator(hero_created_require, name='dispatch')
class HeroOwned(TemplateView):
    template_name = 'game/hero_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hero = get_object_or_404(Hero, user=self.request.user)
        context['hero'] = hero
        context['statistics'] = hero.get_all_statistics()
        return context

    # TODO add option to delete user

@method_decorator(login_required, name='dispatch')
@method_decorator(hero_created_require, name='dispatch')
class HeroDetail(DetailView):
    model = Hero
    template_name = 'game/hero_detail.html'
    context_object_name = 'hero'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hero = Hero.objects.get(user=self.request.user)
        context['statistics'] = hero.get_all_statistics()
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(hero_created_require, name='dispatch')
class HeroList(ListView):
    model = Hero
    template_name = 'game/hero_list.html'
    context_object_name = 'hero_list'
    paginate_by = 30
    
    class Meta:
        ordering = '-name'


# TODO limit max hero limit to 1
@method_decorator(login_required, name='dispatch')
@method_decorator(deny_user_create_more_than_one_hero, name='dispatch')
class CreateHeroView(View):
    def get(self, request, *args, **kwargs):
        hero_form = HeroForm()
        hero_statistics_form = MainStatisticsForm()
        return render(request, 'game/create_hero.html', {
            'hero_form': hero_form,
            'hero_statistics_form': hero_statistics_form,
        })
    
    def post(self, request, *args, **kwargs):
        hero_form = HeroForm(request.POST)
        hero_statistics_form = MainStatisticsForm(request.POST)
        if all([hero_form.is_valid(), hero_statistics_form.is_valid()]):
            hero = Hero.objects.create(
                name=hero_form.cleaned_data['name'],
                user=self.request.user
            )
            self.create_hero_statistics(hero, hero_statistics_form)

            #  TODO maybe instead of rendering success redirect to detail hero view
            return render(request, 'game/success.html', {
                'information': 'Hero created',
            })

    def create_hero_statistics(self, hero, statistics_form):
        for parent_statistic in main_statistics:
            main_statistic = HeroMainStatistic.objects.create(
                name=parent_statistic['name'],
                hero=hero,
                value=statistics_form.cleaned_data[parent_statistic['name']]
            )
            self.create_derivative_statistics(main_statistic, hero)
            
    def create_derivative_statistics(self, parent, hero):
        for derivative_statistic in derivative_statistics:
            if derivative_statistic['parent_name'] == parent.name:
                hero_statistic = HeroDerivativeStatistic.objects.create(
                    name=derivative_statistic['name'],
                    hero=hero,
                    parent=parent,
                    multiplier=derivative_statistic['multiplier'],
                    value=1, # have to pass any value to calculate later
                )
                hero_statistic.calculate_and_save_value()


@method_decorator(login_required, name='dispatch')
@method_decorator(hero_created_require, name='dispatch')
class UpgradeHeroView(FormView):
    statistics = ['strength', 'intelligence', 'agility', 'vitality']
    form_class = MainStatisticsForm
    context_object_name = 'form'
    template_name = 'game/upgrade_hero.html'
    success_url = reverse_lazy('game:main')

    def form_valid(self, form):
        hero = get_object_or_404(Hero, user=self.request.user)
        for statistic_name in self.statistics:
            hero_statistic = hero.get_statistic(statistic_name)
            hero_statistic.value = form.cleaned_data[statistic_name]
            hero_statistic.save()
            self.calculate_new_derivative_statistic_values(hero_statistic)
            
        return super().form_valid(form)

    def calculate_new_derivative_statistic_values(self, hero_main_statistic):
        for derivative_statistic in hero_main_statistic.get_all_derivative_statistics():
            derivative_statistic.calculate_and_save_value()

    def get_initial(self):
        hero = get_object_or_404(Hero, user=self.request.user)
        initial = super().get_initial()
        for statistic in self.statistics:
            value = hero.get_statistic(statistic).value
            initial[statistic] = value
        return initial



@method_decorator(login_required, name='dispatch')
@method_decorator(hero_created_require, name='dispatch')
class FightView(View):

    class Warrior:
        def __init__(self, hero, enemy_hero):
            self.hero = hero
            self.enemy_hero = enemy_hero
            self.health = hero.get_statistic('health').value
            self.max_health = hero.get_statistic('health').value

        def calculate_damage(self):
            enemy_defense = self.enemy_hero.get_statistic('defense').value
            enemy_magic_resist = self.enemy_hero.get_statistic('magic_resist').value

            random_defense_points = randrange(0, math.ceil(enemy_defense / 10))
            random_magic_resist_points = randrange(0, math.ceil(enemy_defense / 10))
            physical_damage = self.hero.get_statistic('physical_damage').value / (enemy_defense + random_defense_points)
            magical_damage = self.hero.get_statistic('magic_attack').value / (enemy_magic_resist + random_magic_resist_points)
            return physical_damage + magical_damage

        def hit(self, opponent):
            # can't assign it in __init__ because it have to change every time
            damage = self.calculate_damage()
            opponent.health -= damage

    def fight(self, attacking_hero, defending_hero):
        # TODO implement critic and dodge chance
        # TODO fight result is always the same (check random defense points)
        # TODO winner have minus health

        attacker = self.Warrior(attacking_hero, defending_hero)
        defender = self.Warrior(defending_hero, attacking_hero)
        while (attacker.health and defender.health) > 0:
            attacker.hit(defender)
            defender.hit(attacker)
        winner = self.choose_winner(attacker, defender)
        return winner

    def choose_winner(self, attacker, defender):
        if attacker.health > defender.health:
            return attacker
        elif attacker.health < defender.health:
            return defender
        else:
            return 'Draw'

    def get(self, request, defender_pk, *args, **kwargs):
        attacking_hero = Hero.objects.get(user=self.request.user)
        defending_hero = get_object_or_404(Hero, pk=defender_pk)
        if attacking_hero == defending_hero:
            return render(request, 'game/information.html', {
                'information': "You can't fight with yourself"
            })
        winner = self.fight(attacking_hero, defending_hero)
        return render(request, 'game/hero_fight.html', {
            'winner': winner
        })
