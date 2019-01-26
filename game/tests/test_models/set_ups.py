from django.test import TestCase
from django.contrib.auth.models import User


class UserSetUp(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user', password='password')
