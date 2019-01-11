from django.test import TestCase
from django.contrib.auth.models import User
from .. import models


class UserSetUp(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user', password='password')
        self.user.save()


class TestHero(UserSetUp):
    def setUp(self):
        super().setUp()
        self.hero = models.Hero.objects.create(
            user=self.user,
            name='hero',
            level = 10,
            experience = 10,
            strength = 10,
            intelligence = 10,
            agility = 10,
            dodge_chance = 10,
            critic_chance = 10,
            health = 10,
            )
        self.hero.save()

    def test_hero_string_representation(self):
        str_repr = "Hero " + self.hero.name
        self.assertEqual(str(self.hero), str_repr)


class TestLocation(TestCase):
    def setUp(self):
        self.location = models.Location.objects.create(name='town')
        self.location.save()

    def test_location_string_representation(self):
        str_repr = "Location " + self.location.name
        self.assertEqual(str(self.location), str_repr)


class TestAction(TestCase):
    def setUp(self):
        self.location = models.Location.objects.create(name='town')
        self.location.save()
        self.action = models.Action.objects.create(name='quest', location=self.location)
        self.action.save()
        
    def test_action_string_representation(self):
        str_repr = "Action " + self.action.name
        self.assertEqual(str(self.action), str_repr)
