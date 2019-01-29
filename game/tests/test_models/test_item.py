from ...models.hero import Hero, add_item_stats, remove_item_stats, calculate_stats
from ...models.item import Item
from .set_ups import UserSetUp, ItemFunctionsSetUp

class TestItem(UserSetUp):
    def setUp(self):
        super().setUp()
        self.hero = Hero.objects.create(
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
        self.item = Item.objects.create(name='axe', owner=self.hero)
        self.item.save()

    def test_item_string_representation(self):
        str_repr = "Item " + self.item.name
        self.assertEqual(str(self.item), str_repr)


class TestItemFunctions(ItemFunctionsSetUp):
    def setUp(self):
        super().setUp()
        self.hero = self.create_hero()
        self.initial_stats = 10
        self.items = []
        self.items.append(self.create_items(10))

    def test_add_item_stats(self):
        add_item_stats(self.hero)

        """ TODO Pull this code out of method (it repeats in remove method)"""
        items_strength = 0
        items_intelligence = 0
        items_agility = 0
        items_vitality = 0
        for item in self.hero.item_set.all():
            items_strength += item.strength
            items_intelligence += item.intelligence
            items_agility += item.agility
            items_vitality += item.vitality

        # had to reload hero object
        self.reload_hero_instance()
            
        self.assertEqual(self.hero.strength, self.initial_stats + items_strength)
        self.assertEqual(self.hero.intelligence, (self.initial_stats + items_intelligence))
        self.assertEqual(self.hero.agility, (self.initial_stats + items_agility))
        self.assertEqual(self.hero.vitality, (self.initial_stats + items_vitality))

    def test_remove_item_stats(self):
        add_item_stats(self.hero)
        self.reload_hero_instance()
        remove_item_stats(self.hero)
        self.reload_hero_instance()

        items_strength = 0
        items_intelligence = 0
        items_agility = 0
        items_vitality = 0
        for item in self.hero.item_set.all():
            items_strength += item.strength
            items_intelligence += item.intelligence
            items_agility += item.agility
            items_vitality += item.vitality

        # had to reload hero object
        self.reload_hero_instance()
            
        self.assertEqual(self.initial_stats, self.hero.strength)
        self.assertEqual(self.initial_stats, self.hero.intelligence)
        self.assertEqual(self.initial_stats, self.hero.agility)
        self.assertEqual(self.initial_stats, self.hero.vitality)

    def test_calculate_stats(self):
        calculate_stats(self.hero)
        self.hero = Hero.objects.get(pk=self.hero.pk)
        self.assertEqual(self.hero.defense, self.hero.strength * 0.5)
        self.assertEqual(self.hero.physical_attack, self.hero.strength * 1.5)
        self.assertEqual(self.hero.magic_attack, self.hero.intelligence * 1.5)
        self.assertEqual(self.hero.magic_resist, self.hero.intelligence * 0.5)
        self.assertEqual(self.hero.dodge_chance, self.hero.agility * 0.0025)
        self.assertEqual(self.hero.critic_chance, self.hero.agility * 0.005)
        self.assertEqual(self.hero.health, self.hero.vitality * 5.0)

