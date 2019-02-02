import random
from django.test import TestCase
from django.contrib.auth.models import User
from ...models.hero import Hero
from ...models.item import Item


class UserSetUp(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user', password='password')
