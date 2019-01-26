from django.test import TestCase
from django.contrib.auth.models import User
from ...models import Hero, Fighter


class TestFighter(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="user", password="password")
        self.enemy_user = User.objects.create(username="enemy_user", password="password")
        self.hero = self.create_hero(self.user, 'hero', 10)
        self.enemy_hero = self.create_hero(self.enemy_user, 'enemy_hero', 5)
        self.attacking_fighter = Fighter(self.hero, self.enemy_hero)

    def create_hero(self, owner, name, stats):
        """
            This code won't work, in variable memory is still instace
            before post_save signal.

            hero = Hero.objects.create(
                ...
            )
        """
        Hero.objects.create(
            owner=owner,
            name=name,
            level=stats,
            experience=stats,
            strength=stats,
            intelligence=stats,
            agility=stats,
            vitality=stats,
        )

        # Reload
        hero = Hero.objects.get(owner=owner)
        return hero

    def test_calculate_physical_damage(self):
        physical_dmg = self.hero.physical_attack / self.enemy_hero.defense
        self.assertEqual(physical_dmg, self.attacking_fighter.physical_damage)

    def test_calculate_magical_damage(self):
        magical_dmg = self.hero.magic_attack / self.enemy_hero.magic_resist
        self.assertEqual(magical_dmg, self.attacking_fighter.magical_damage)
    
    def test_hit_enemy(self):
        enemy_health = self.enemy_hero.health
        total_damage = self.attacking_fighter.physical_damage + self.attacking_fighter.magical_damage
        self.attacking_fighter.hit_enemy(self.enemy_hero)
        enemy_health_after_hit = enemy_health - total_damage
        self.assertEqual(enemy_health_after_hit, self.enemy_hero.health)
    