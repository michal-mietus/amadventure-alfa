from itertools import chain
from django.test import TestCase, Client, RequestFactory
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from ..models.hero import Hero
from ..models.statistics import HeroMainStatistic, HeroDerivativeStatistic
from ..forms import MainStatisticsForm
from ..statistic_properties import derivative_statistics
from .. import views


class UserSetUp(TestCase):
    def setUp(self):
        self.username = 'username'
        self.password = 'password'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
        )
        self.client = Client()
        self.factory = RequestFactory()

    def login_user(self):
        self.client.login(username=self.username, password=self.password)
    

class UserAndHeroSetUp(UserSetUp):
    def setUp(self):
        super().setUp()
        self.hero = Hero.objects.create(
            user=self.user,
            name='hero_name',
        )


class TestMainView(UserSetUp):
    def setUp(self):
        super().setUp()
        self.app_name = 'game'
        self.url_name = 'main'

    def test_access_main(self):
        self.login_user()
        url = self.app_name + ':' + self.url_name
        response = self.client.get(reverse(url))
        self.assertTemplateUsed('main.html')

    def test_get_return(self):
        response = self.client.get(reverse(self.app_name + ':' + self.url_name))
        self.assertTemplateUsed('main.html')
    

class TestCreateHeroView(UserAndHeroSetUp):
    def setUp(self):
        super().setUp()
        self.app_name = 'game'
        self.url_name = 'create_hero'
        self.url = self.app_name + ':' + self.url_name
        self.view = views.CreateHeroView()

    def test_prevent_logged_user_access_create_hero_view(self):
        response = self.client.get(reverse(self.url))
        redirect_url = reverse('usersystem:sign_in') + '?next=' + reverse(self.url)
        self.assertRedirects(response, redirect_url)

    def test_allow_logged_user_access_create_hero_view(self):
        self.login_user()
        response = self.client.get(reverse(self.url))
        self.assertTemplateUsed('create_hero.html')

    def test_create_hero_statistics_method(self):
        data = {
            'strength': 10,
            'intelligence': 10,
            'agility': 10,
            'vitality': 10,
        }
        request = self.factory.post(reverse('game:create_hero'), data=data)
        form = MainStatisticsForm(request.POST)
        form.is_valid()
        self.view.create_hero_statistics(hero=self.hero, statistics_form=form)
        all_statistics = self.hero.heromainstatistic_set.all()
        self.assertQuerysetEqual(
            HeroMainStatistic.objects.all(), 
            all_statistics,
            transform=lambda x: x,
            ordered=False
        )

    def test_create_derivative_statistics_method(self):
        parent_statistic = HeroMainStatistic.objects.create(
            name='strength',
            value=10,
            hero=self.hero
        )
        self.view.create_derivative_statistics(parent_statistic, self.hero)
        statistic_count = 0
        for statistic in derivative_statistics:
            if statistic['parent_name'] == parent_statistic.name:
                statistic_count += 1

        self.assertEqual(len(HeroDerivativeStatistic.objects.all()), statistic_count)


class TestUpgradeHeroView(UserSetUp):
    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()
        self.app_name = 'game'
        self.url_name = 'upgrade_hero'
        self.url = self.app_name + ':' + self.url_name
        self.view = views.UpgradeHeroView()
    
    def test_prevent_logged_user_access_upgrade_view(self):
        response = self.client.get(reverse(self.url))
        url =  reverse('usersystem:sign_in') + '?next=' + reverse('game:upgrade_hero')
        self.assertRedirects(response, url)

    def test_allow_logged_user_access_upgrade_view(self):
        self.login_user()
        response = self.client.get(reverse(self.url))
        self.assertTemplateUsed('upgrade_hero.html')

    def test_if_user_dont_have_hero_redirect_to_create_hero_view(self):
        self.login_user()
        response = self.client.get(reverse(self.url))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('game:create_hero'))

    def test_form_valid_upgrade_hero(self):
        self.login_user()
        hero = self.create_hero()
        self.create_hero_statistics(hero)
        statistics = {
            'strength': 10,
            'intelligence': 10,
            'agility': 10,
            'vitality': 10
        }

        response = self.client.post(reverse(self.url), statistics)
        self.assertEqual(response.status_code, 302)
        all_statistics = list(chain(HeroMainStatistic.objects.filter(hero=hero), HeroDerivativeStatistic.objects.filter(hero=hero)))
        self.assertQuerysetEqual(
            hero.get_all_statistics(), 
            HeroMainStatistic.objects.filter(hero=hero),
            transform=lambda x: x,
            ordered=False,
        )
    
    def test_calculate_new_derivative_statistic_values(self):
        hero = self.create_hero()
        create_hero_view = views.CreateHeroView()
        parent_stat = HeroMainStatistic.objects.create(
            name='strength',
            value=10,
            hero=hero
        )
        create_hero_view.create_derivative_statistics(parent_stat, hero)
        value_after_upgrade = 20
        parent_stat.value = value_after_upgrade
        parent_stat.save()
        self.view.calculate_new_derivative_statistic_values(parent_stat)
        for derivative_statistic in derivative_statistics:
            if derivative_statistic['parent_name'] == parent_stat.name:
                der_stat = HeroDerivativeStatistic.objects.get(name=derivative_statistic['name'])
                self.assertEqual(der_stat.value, value_after_upgrade * derivative_statistic['multiplier'])


    def test_upgrade_hero_view_initial_value(self):
        hero = self.create_hero()
        self.create_hero_statistics(hero)
        request = self.factory.get(reverse('game:upgrade_hero'))
        request.user = self.user
        view = views.UpgradeHeroView()
        view.request = request
        initial_returned = view.get_initial()
        statistic_names = ['strength', 'intelligence', 'agility', 'vitality']
        for statistic_name in statistic_names:
            self.assertEqual(initial_returned[statistic_name], 10)

    def create_hero_statistics(self, hero):
        statistic_names = ['strength', 'intelligence', 'agility', 'vitality']
        for statistic_name in statistic_names:
            HeroMainStatistic.objects.create(
                hero=hero,
                name=statistic_name,
                value=10
            )

    def create_hero(self):
        return Hero.objects.create(
            name='hero_name',
            user=self.user
        )


class TestHeroDetailView(UserAndHeroSetUp):
    def test_returned_context_data(self):
        factory = RequestFactory()
        request = factory.get(reverse('game:hero_detail', kwargs={'pk': self.hero.pk}))
        request.user = self.user
        response = views.HeroDetail.as_view()(request, pk=self.hero.pk)
        self.assertQuerysetEqual(response.context_data['statistics'], self.hero.get_all_statistics())


class TestHeroOwnedView(UserSetUp):
    def test_access_page_without_created_hero_returns_create_hero_view(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('game:hero_owned'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'game/create_hero.html')

    def test_access_page_without_created_hero_redirect(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('game:hero_owned'))
        self.assertEqual(response.status_code, 302)

    def test_valid_access_page_with_created_hero(self):
        hero = Hero.objects.create(name='hero_name', user=self.user)
        self.create_hero_statistics(hero)
        self.login_user()
        response = self.client.get(reverse('game:hero_owned'))
        self.assertEqual(response.context['hero'], hero)
        hero_statistics = hero.get_all_statistics()
        self.assertQuerysetEqual(
            response.context['statistics'], 
            hero_statistics,
            transform=lambda x: x,
            ordered=False
        )

    def create_hero_statistics(self, hero):
        statistic_names = ['strength', 'intelligence', 'agility', 'vitality']
        for statistic_name in statistic_names:
            HeroMainStatistic.objects.create(
                hero=hero,
                name=statistic_name,
                value=10
            )
