from ...models.hero import Hero
from ...models.item import Item
from ...models.statistic import HeroStatistic
from ...models.statistic import ItemStatistic
from .set_ups import UserSetUp


class TestHero(UserSetUp):
    def setUp(self):
        super().setUp()
        self.hero = Hero.objects.create(
            user=self.user,
            name='hero'
        )
        self.statistic_properties = {
            'name': 'strength',
            'parent': None,
            'multiplier': 1,
            'value': 10,
            'owner': self.hero
        }

    def test_valid_create_hero(self):
        hero = Hero.objects.create(
            user=self.user,
            name='hero'
        )

    def test_hero_str_representation(self):
        self.assertEqual(str(self.hero), "Hero hero") 

    def test_get_all_items(self):
        item = Item.objects.create(name='item', owner=self.hero)
        hero_items = self.hero.item_set.all()
        self.assertQuerysetEqual(
            hero_items, 
            self.hero.get_all_items(), 
            transform=lambda x: x,
            ordered=False
        )

    def test_get_statistic(self):
        statistic = HeroStatistic.objects.create(**self.statistic_properties)
        result = self.hero.get_statistic(self.statistic_properties['name'])
        self.assertEqual(statistic, result)

    def test_get_all_statistics(self):
        statistic = HeroStatistic.objects.create(**self.statistic_properties)
        result = self.hero.get_all_statistics()
        self.assertEqual(result[0], statistic)

    def test_remove_item_statistic(self):
        hero_statistic = HeroStatistic(**self.statistic_properties).save()
        item = Item.objects.create(name='item', owner=self.hero)
        item_statistic = ItemStatistic.objects.create(name='strength', value=5, owner=item)
        hero_statistic_before_remove = self.hero.get_statistic(self.statistic_properties['name'])
        self.hero.remove_item_statistic(item_statistic)
        current_statistic_value = self.hero.get_statistic(self.statistic_properties['name']).value
        hero_statistic_difference = hero_statistic_before_remove.value - current_statistic_value
        self.assertEqual(hero_statistic_difference, item_statistic.value)

    def test_add_item_statistic(self):
        hero_statistic = HeroStatistic(**self.statistic_properties).save()
        item = Item.objects.create(name='item', owner=self.hero)
        item_statistic = ItemStatistic.objects.create(name='strength', value=5, owner=item)
        hero_statistic_before_remove = self.hero.get_statistic(self.statistic_properties['name'])
        self.hero.add_item_statistic(item_statistic)
        current_statistic_value = self.hero.get_statistic(self.statistic_properties['name']).value
        hero_statistic_difference = current_statistic_value - hero_statistic_before_remove.value
        self.assertEqual(hero_statistic_difference, item_statistic.value)
       
