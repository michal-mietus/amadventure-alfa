from ...models.statistic import Statistic
from ...models.new_hero import NewHero
from ...models.new_item import NewItem
from .set_ups import UserSetUp


class TestNewItem(UserSetUp):
    def setUp(self):
        super().setUp()
        self.hero = NewHero.objects.create(
            name='hero',
            user=self.user,
        )
        self.item = NewItem.objects.create(
            name='item',
            owner=self.hero,
        )

    def test_valid_create_item(self):
        hero = NewHero.objects.create(
            name='hero',
            user=self.user,
        )
        item = NewItem.objects.create(
            name='item',
            owner=hero,
        )
