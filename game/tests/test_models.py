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
            owner=self.user,
            name='hero',
            level = 10,
            experience = 10,
            strength = 10,
            intelligence = 10,
            agility = 10,
            vitality = 10,
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


class TestItem(UserSetUp):
    def setUp(self):
        super().setUp()
        self.hero = models.Hero.objects.create(
            owner=self.user,
            name='hero',
            level = 10,
            experience = 10,
            strength = 10,
            intelligence = 10,
            agility = 10,
            vitality = 10,
            )
        self.hero.save()
        self.item = models.Item.objects.create(name='axe', owner=self.hero)
        self.item.save()

    def test_item_string_representation(self):
        str_repr = "Item " + self.item.name
        self.assertEqual(str(self.item), str_repr)


class TestItemFunctions(UserSetUp):
    def setUp(self):
        super().setUp()
        self.strength = 10
        self.intelligence = 10
        self.agility = 10
        self.vitality = 10
        self.hero = self.create_hero()

        self.item_strength = 2
        self.item_intelligence = 2
        self.item_agility = 2
        self.item_vitality = 2
        item = self.create_item()

    def create_hero(self):
        hero = models.Hero.objects.create(
            owner=self.user,
            name='hero',
            level = 10,
            experience = 10,
            strength = self.strength,
            intelligence = self.intelligence,
            agility = self.agility,
            vitality = self.vitality,
        )
        return hero

    def create_item(self):
        item = models.Item.objects.create(
            name='axe',
            owner=self.hero,
            strength=self.item_strength,
            intelligence=self.item_intelligence,
            agility=self.item_agility,
            vitality=self.item_vitality,
        )
        return item

    def test_add_item_stats(self):
        models.add_item_stats(self.hero)
        items_strength = 0
        items_intelligence = 0
        items_agility = 0
        items_vitality = 0
        for item in self.hero.item_set.all():
            items_strength += item.strength
            items_intelligence = item.intelligence
            items_agility += item.agility
            items_vitality += item.vitality

        # had to reload hero object
        self.hero = models.Hero.objects.get(owner=self.user)
            
        self.assertEqual(self.hero.strength, self.strength + items_strength)
        self.assertEqual(self.hero.intelligence, self.intelligence + items_intelligence)
        self.assertEqual(self.hero.agility, self.agility + items_agility)
        self.assertEqual(self.hero.vitality, self.vitality + items_vitality)

    def test_remove_item_stats(self):
        models.remove_item_stats(self.hero)
        items_strength = 0
        items_intelligence = 0
        items_agility = 0
        items_vitality = 0
        for item in self.hero.item_set.all():
            items_strength += item.strength
            items_intelligence = item.intelligence
            items_agility += item.agility
            items_vitality += item.vitality

        # had to reload hero object
        self.hero = models.Hero.objects.get(owner=self.user)
            
        self.assertEqual(self.hero.strength, self.strength - items_strength)
        self.assertEqual(self.hero.intelligence, self.intelligence - items_intelligence)
        self.assertEqual(self.hero.agility, self.agility - items_agility)
        self.assertEqual(self.hero.vitality, self.vitality - items_vitality)

    def test_calculate_stats(self):
        models.calculate_stats(self.hero)
        self.hero = models.Hero.objects.get(pk=self.hero.pk)
        self.assertEqual(self.hero.defense, self.hero.strength * 1.0)
        self.assertEqual(self.hero.physical_attack, self.hero.strength * 3.0)
        self.assertEqual(self.hero.magic_attack, self.hero.intelligence * 3.0)
        self.assertEqual(self.hero.magic_resist, self.hero.intelligence * 1.0)
        self.assertEqual(self.hero.dodge_chance, self.hero.agility * 0.0025)
        self.assertEqual(self.hero.critic_chance, self.hero.agility * 0.005)
        self.assertEqual(self.hero.health, self.hero.vitality * 5.0)