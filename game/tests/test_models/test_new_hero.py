from ...models.statistic import Statistic
from ...models.new_hero import NewHero
from ...models.new_item import NewItem
from .set_ups import UserSetUp


class TestNewHero(UserSetUp):
    def test_valid_create_hero(self):
        hero = NewHero.objects.create(
            user=self.user,
            name='hero'
        )
