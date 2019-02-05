from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import TemplateView, DetailView
from django.views.generic.base import ContextMixin, View
from django.views.generic.edit import FormView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .decorators import hero_created_require, logged_user_redirect_to_main_view, deny_user_create_more_than_one_hero
from .forms import HeroForm, HeroStatisticsForm
from .models.hero import Hero
from .models.item import Item
from .models.statistic import HeroStatistic


class HeroGetPkContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            hero = Hero.objects.get(user=self.request.user)
            context['hero_pk'] = hero.pk
        except Exception as e:
            context['hero_pk'] = False
        return context


@method_decorator(logged_user_redirect_to_main_view, name='dispatch')
class WelcomeView(TemplateView):
    template_name = 'game/amadventure.html'


@method_decorator(login_required, name='dispatch')
class MainView(TemplateView, HeroGetPkContextMixin):
    template_name = 'game/main.html'


@method_decorator(login_required, name='dispatch')
@method_decorator(hero_created_require, name='dispatch')
class HeroDetail(DetailView, HeroGetPkContextMixin):
    model = Hero
    template_name = 'game/hero_detail.html'
    context_object_name = 'hero'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hero = Hero.objects.get(user=self.request.user)
        context['statistics'] = hero.get_all_statistics()
        return context


# TODO limit max hero limit to 1
@method_decorator(login_required, name='dispatch')
@method_decorator(deny_user_create_more_than_one_hero, name='dispatch')
class CreateHeroView(View, HeroGetPkContextMixin):
    def get(self, request, *args, **kwargs):
        hero_form = HeroForm()
        hero_statistics_form = HeroStatisticsForm()
        return render(request, 'game/create_hero.html', {
            'hero_form': hero_form,
            'hero_statistics_form': hero_statistics_form,
        })
    
    def post(self, request, *args, **kwargs):
        statistics = ['strength', 'intelligence', 'agility', 'vitality']
        hero_form = HeroForm(request.POST)
        hero_statistics_form = HeroStatisticsForm(request.POST)
        if all([hero_form.is_valid(), hero_statistics_form.is_valid()]):
            user = User.objects.get(pk=request.user.pk)
            hero = Hero(
                name = hero_form.cleaned_data['name'],
                user = user
            )
            hero.save()
            hero = Hero.objects.filter(user=request.user)[0] # reload

            for statistic_name in statistics:
                hero_statistic = HeroStatistic(
                    name=statistic_name,
                    owner=hero,
                    value=hero_statistics_form.cleaned_data[statistic_name]
                )
                hero_statistic.save()
            #  TODO maybe instead of rendering success redirect to detail hero view
        return render(request, 'game/success.html', {
            'information': 'Hero created',
        })


@method_decorator(login_required, name='dispatch')
@method_decorator(hero_created_require, name='dispatch')
class UpgradeHeroView(FormView, HeroGetPkContextMixin):
    statistics = ['strength', 'intelligence', 'agility', 'vitality']
    form_class = HeroStatisticsForm
    context_object_name = 'form'
    template_name = 'game/upgrade_hero.html'
    success_url = reverse_lazy('game:main')

    def form_valid(self, form):
        hero = get_object_or_404(Hero, user=self.request.user)
        for statistic_name in self.statistics:
            hero_statistic = hero.get_statistic(statistic_name)
            hero_statistic.value = form.cleaned_data[statistic_name]
            hero_statistic.save()
        return super().form_valid(form)

    def get_initial(self):
        hero = get_object_or_404(Hero, user=self.request.user)
        initial = super().get_initial()
        for statistic in self.statistics:
            value = hero.get_statistic(statistic).value
            initial[statistic] = value
        return initial
