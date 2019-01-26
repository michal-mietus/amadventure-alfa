from ...models import Hero
from .set_ups import UserSetUp

class TestHero(UserSetUp):
    def setUp(self):
        super().setUp()
        self.hero = Hero.objects.create(
            owner=self.user,
            name='hero',
            level=10,
            experience=10,
            strength=10,
            intelligence=10,
            agility=10,
            vitality=10,
            )
        self.hero.save()

    def test_hero_string_representation(self):
        str_repr = "Hero " + self.hero.name
        self.assertEqual(str(self.hero), str_repr)