from ...models.statistics import ItemMainStatistic, ItemDerivativeStatistic
from ...models.hero import Hero
from ...models.item import Item
from .set_ups import UserSetUp
from itertools import chain


class TestItem(UserSetUp):
    def setUp(self):
        super().setUp()
        self.hero = Hero.objects.create(
            name='hero',
            user=self.user,
        )
        self.item = Item.objects.create(
            name='item',
            owner=self.hero,
        )

    def test_valid_create_item(self):
        hero = Hero.objects.create(
            name='hero',
            user=self.user,
        )
        item = Item.objects.create(
            name='item',
            owner=hero,
        )

    def test_item_str_represenatation(self):
        name = 'name'
        item = Item.objects.create(
            name=name,
            owner=self.hero,
        )

        self.assertEqual(str(item), "Item " + name)

    def test_valid_get_all_statistics(self):
        strength_statistic = ItemMainStatistic.objects.create(
            name='strength',
            value=10,
            item=self.item
        )
        agility_statistic = ItemMainStatistic.objects.create(
            name='agility',
            value=10,
            item=self.item
        )
        
        self.assertQuerysetEqual(
            list(chain(self.item.itemmainstatistic_set.all(), self.item.itemderivativestatistic_set.all())),
            self.item.get_all_list_statistics(), 
            transform=lambda x: x,
            ordered=False,
        )
