import random
from django.test import TestCase
from django.contrib.auth.models import User
from ...models import Hero, Item


class UserSetUp(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user', password='password')


class ItemFunctionsSetUp(UserSetUp):
    def create_hero(self):
        hero = Hero.objects.create(
            owner=self.user,
            name='hero',
            level = 10,
            experience = 10,
            strength = 10,
            intelligence = 10,
            agility = 10,
            vitality = 10,
        )
        return hero

    def create_item(self, name, owner, stats):
        item = Item.objects.create(
            name=name,
            owner=owner,
            strength=stats,
            intelligence=stats,
            agility=stats,
            vitality=stats,
        )
        return item

    def create_items(self, quantity):
        items = []
        for i in range(quantity):
            statistics = random.randint(1, 50)
            items.append(self.create_item('item_name', self.hero, statistics))
        return items

    def reload_hero_instance(self):
        self.hero = Hero.objects.get(owner=self.user)