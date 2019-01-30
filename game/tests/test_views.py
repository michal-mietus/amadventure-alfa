from django.test import TestCase, Client
from django.shortcuts import reverse
from django.contrib.auth.models import User
from ..models.hero import Hero


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
        self.url_name = 'hero_create'
        self.url = self.app_name + ':' + self.url_name

    def test_prevent_logged_user_access_main(self):
        response = self.client.get(reverse(self.url))
        self.assertRedirects(response, '/user/sign_in/?next=/hero_create/')

    def test_allow_logged_user_access_main(self):
        self.login_user()
        response = self.client.get(reverse(self.url))
        self.assertTemplateUsed('create_hero.html')


class TestHeroUpgradeView(UserSetUp):
    def setUp(self):
        super().setUp()
        self.app_name = 'game'
        self.url_name = 'hero_upgrade'
        self.url = self.app_name + ':' + self.url_name
    
    def test_prevent_logged_user_access_upgrade_view(self):
        response = self.client.get(reverse(self.url))
        self.assertRedirects(response, '/user/sign_in/?next=/hero_upgrade/')

    def test_allow_logged_user_access_upgrade_view(self):
        self.login_user()
        response = self.client.get(reverse(self.url))
        self.assertTemplateUsed('upgrade_hero.html')
