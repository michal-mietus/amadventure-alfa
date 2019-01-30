from django.shortcuts import render, reverse, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import HeroForm, HeroStatisticsForm
from .models.hero import Hero
from .models.item import Item
from .models.statistic import HeroStatistic
from .decorators import hero_created_require, logged_user_redirect_to_main_view


@method_decorator(logged_user_redirect_to_main_view, name='dispatch')
class WelcomeView(TemplateView):
    template_name = 'game/amadventure.html'


@method_decorator(login_required, name='dispatch')
class MainView(TemplateView):
    template_name = 'game/main.html'


@method_decorator(login_required, name='dispatch')
class HeroCreateView(FormView):
    template_name = 'game/create_hero.html'
    form_class = HeroForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('game:main')


# why decorator works but overriding method and super() call doesnt
# decorator order is important!
@method_decorator(login_required, name='dispatch')
@method_decorator(hero_created_require, name='dispatch')
class HeroUpgradeView(UpdateView):
    template_name = 'game/upgrade_hero.html'
    model = Hero

    def get_object(self, queryset=None):
        # TODO how get current hero (if we would have more than one to choose)?
        obj = Hero.objects.get(user=self.request.user)
        return obj

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('game:main')


def create_hero(request):
    if request.method == 'POST':
        # TODO pass arguments to statistic and hero models
        statistics = ['strength', 'intelligence', 'agility', 'vitality']
        hero_form = HeroForm(request.POST)
        hero_statistics_form = HeroStatisticsForm(request.POST)
        if all([hero_form.is_valid(), hero_statistics_form.is_valid()]):
            hero = Hero(
                name = hero_form.cleaned_data['name'],
                user = request.user
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


        return render(request, 'game/success.html', {
            'information': 'User created'
        })
    else:
        hero_form = HeroForm()
        hero_statistics_form = HeroStatisticsForm()
        return render(request, 'game/create_hero.html', {
            'hero_form': hero_form,
            'hero_statistics_form': hero_statistics_form
        })
