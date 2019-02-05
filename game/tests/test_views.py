from django.test import TestCase, Client, RequestFactory
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from ..models.hero import Hero
from ..models.statistic import HeroStatistic
from .. import views



class UserSetUp(TestCase):
    def setUp(self):
        self.username = 'username'
        self.password = 'password'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )
        self.client = Client()

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

    def test_prevent_logged_user_access_main(self):
        url = self.app_name + ':' + self.url_name
        response = self.client.get(reverse(url))
        self.assertRedirects(response, '/user/sign_in/?next=/main/')

    def test_allow_logged_user_access_main(self):
        self.login_user()
        url = self.app_name + ':' + self.url_name
        response = self.client.get(reverse(url))
        self.assertTemplateUsed('main.html')

    def test_get_return(self):
        response = self.client.get(reverse(self.app_name + ':' + self.url_name))
        self.assertTemplateUsed('main.html')
    

class TestHeroCreateView(UserSetUp):
    def setUp(self):
        super().setUp()
        self.app_name = 'game'
        self.url_name = 'create_hero'
        self.url = self.app_name + ':' + self.url_name

    def test_prevent_logged_user_access_create_hero_view(self):
        response = self.client.get(reverse(self.url))
        self.assertRedirects(response, '/user/sign_in/?next=/create_hero/')

    def test_allow_logged_user_access_create_hero_view(self):
        self.login_user()
        response = self.client.get(reverse(self.url))
        self.assertTemplateUsed('create_hero.html')


class TestUpgradeHeroView(UserSetUp):
    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()
        self.app_name = 'game'
        self.url_name = 'upgrade_hero'
        self.url = self.app_name + ':' + self.url_name
    
    def test_prevent_logged_user_access_upgrade_view(self):
        response = self.client.get(reverse(self.url))
        self.assertRedirects(response, '/user/sign_in/?next=/upgrade_hero/')

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
        hero = Hero.objects.create(
            name='hero name',
            user=self.user
        )
        self.create_hero_statistics(hero)
        statistics = {
            'strength': 10,
            'intelligence': 10,
            'agility': 10,
            'vitality': 10
        }

        response = self.client.post(reverse(self.url), statistics)
        self.assertEqual(response.status_code, 302)
        self.assertQuerysetEqual(
            hero.get_all_statistics(), 
            HeroStatistic.objects.filter(owner=hero),
            transform=lambda x: x,
            ordered=False,
        )

    def test_upgrade_hero_view_initial_value(self):
        hero = Hero.objects.create(
            name='hero_name',
            user=self.user
        )
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
            HeroStatistic.objects.create(
                owner=hero,
                name=statistic_name,
                value=10
            )


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
            HeroStatistic.objects.create(
                owner=hero,
                name=statistic_name,
                value=10
            )

