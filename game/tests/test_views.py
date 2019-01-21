from django.test import TestCase, Client
from django.shortcuts import reverse
from django.contrib.auth.models import User
from ..models import Hero


class UserSetUp(TestCase):
    def setUp(self):
        self.username = 'username'
        self.password = 'password'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )
        self.client = Client()


class TestMainView(UserSetUp):
    def setUp(self):
        super().setUp()
        self.app_name = 'game'
        self.url_name = 'main'

    def test_prevent_logged_user_access_main(self):
        url = self.app_name + ':' + self.url_name
        response = self.client.get(reverse(url))
        self.assertRedirects(response, '/user/sign_in/?next=/')

    def test_allow_logged_user_access_main(self):
        self.client.login(username=self.username, password=self.password)
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
        self.hero_object = {
            'name':' hero_name',
            'strength': 10,
            'intelligence': 10,
            'agility': 10,
            'vitality': 10
        }

    def test_prevent_logged_user_access_main(self):
        response = self.client.get(reverse(self.url))
        self.assertRedirects(response, '/user/sign_in/?next=/hero_create/')

    def test_allow_logged_user_access_main(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse(self.url))
        self.assertTemplateUsed('create_hero.html')

    def test_valid_create_hero(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse(self.url), data=self.hero_object)
        self.assertEqual(response.status_code, 302)

    def test_invalid_create_hero(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse(self.url), data={
            'name':' hero_name',
            'strength': None,
            'intelligence': 'asddas',
            'agility': 10,
            'vitality': 10
        })        
        self.assertEqual(response.status_code, 200)

    
