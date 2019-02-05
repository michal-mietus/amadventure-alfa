from django.test import TestCase, Client
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from ..models.hero import Hero
from ..models.statistic import HeroStatistic
from ..views import HeroGetPkContextMixin


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


class TestHeroGetPkContextMixin(UserAndHeroSetUp):
    class TestView(HeroGetPkContextMixin, TemplateView):
        pass

    def test_get_context_data(self):
        view = self.TestView()
        context = view.get_context_data()
        self.assertEqual(context['hero_pk'], False)

    # TODO how pass to method request, if cant call view as link


class TestHeroDetailView(UserAndHeroSetUp):
    def test_get_context_data(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('game:hero_detail', kwargs={'pk':self.hero.pk}))
        self.assertQuerysetEqual(response.context['statistics'], self.hero.get_all_statistics())


class TestCreateHeroView(UserSetUp):
    def test_valid_create_hero_post_data(self):
        self.client.login(username=self.username, password=self.password)
        name = {'name': 'created_hero'}
        statistics = {
            'strength': 10,
            'intelligence': 10,
            'agility': 10,
            'vitality': 10
        }
        data_to_send = {**name, ** statistics}
        response = self.client.post(reverse('game:create_hero'), data_to_send)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'game/success.html')
        created_hero = Hero.objects.get(name='created_hero')
        self.assertEqual(created_hero.user, self.user)
        self.assertEqual(created_hero.name, 'created_hero')
        for name, value in statistics.items():
            hero_statistic = created_hero.get_statistic(name)
            self.assertEqual(value, hero_statistic.value)
        
    def test_is_user_has_hero_redirect_to_main(self):
        self.hero = Hero.objects.create(
            name='hero',
            user=self.user
        )
        name = {'name': 'created_hero'}
        statistics = {
            'strength': 10,
            'intelligence': 10,
            'agility': 10,
            'vitality': 10
        }
        data_to_send = {**name, ** statistics}
        response = self.client.post(reverse('game:create_hero'), data_to_send)
        self.assertEqual(response.status_code, 302)
