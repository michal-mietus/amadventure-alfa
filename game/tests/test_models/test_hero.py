from django.contrib.auth.models import User
from ...models import Hero, Fighter
from .set_ups import UserSetUp

class TestHero(UserSetUp):
    def setUp(self):
        super().setUp()
        Hero.objects.create(
            owner=self.user,
            name='hero',
            level=10,
            experience=10,
            strength=10,
            intelligence=10,
            agility=10,
            vitality=10,
            )
        self.hero = Hero.objects.get(owner=self.user)

    def test_hero_string_representation(self):
        str_repr = "Hero " + self.hero.name
        self.assertEqual(str(self.hero), str_repr)

    def test_choose_winner_hero_win(self):
        enemy_user = User.objects.create(username="enemy_user", password="password")
        Hero.objects.create(
            owner=enemy_user,
            name="enemy_heor",
            strength=3,
            intelligence=3,
            agility=3,
            vitality=3
        )
        enemy_hero = Hero.objects.get(owner=enemy_user)
        fighter = Fighter(self.hero, enemy_hero)
        enemy_fighter = Fighter(enemy_hero, self.hero)
        self.assertTrue(fighter.health > enemy_fighter.health)
        result = self.hero.choose_winner(fighter, enemy_fighter)
        self.assertEqual(result, "Attacker won")

    # TODO choose winner when attacker lose
