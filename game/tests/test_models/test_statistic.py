from ...models.statistics import  HeroMainStatistic, ItemMainStatistic, HeroDerivativeStatistic, ItemDerivativeStatistic
from ...models.hero import Hero
from ...models.item import Item
from .set_ups import UserSetUp


class TestHeroMainStatistic(UserSetUp):
    def setUp(self):
        super().setUp()
        self.hero = Hero.objects.create(
            name='hero_name',
            user=self.user
        )

    def test_statistic_string_representation(self):
        statistic = HeroMainStatistic.objects.create(
            hero=self.hero,
            name='statistic_name',
            value=10,
        )
        str_repr = "Main statistic " + statistic.name
        self.assertEqual(str(statistic), str_repr)

    def test_create_statistics(self):
        statistics_pairs = {
            'Strength': 10,
            'Intelligence': 5,
            'Agility': 7,
            'Vitality': 6,
        }
        for name, value in statistics_pairs.items():
            HeroMainStatistic.objects.create(
                hero=self.hero,
                name=name,
                value=value,
            )


class TestDerivativeStatistic(UserSetUp):
    def setUp(self):
        super().setUp()
        self.hero = Hero.objects.create(
            name='hero_name',
            user=self.user,
        )
        self.main_statistic = HeroMainStatistic.objects.create(
            name='strength',
            value=10,
            hero=self.hero,
        )
        self.derivative_statistic = HeroDerivativeStatistic.objects.create(
            name='attack',
            multiplier=2,
            hero=self.hero,
            parent=self.main_statistic,
        )

    def test_statistic_string_representation(self):
        str_repr = "Hero derivative statistic " + self.derivative_statistic.name
        self.assertEqual(str(self.derivative_statistic), str_repr)

    def test_calculate_value(self):
        self.derivative_statistic.calculate_and_save_value()
        value = self.derivative_statistic.parent.value * self.derivative_statistic.multiplier
        self.assertEqual(self.derivative_statistic.value, value)


class TestHeroDerivativeStatistic(UserSetUp):
    def setUp(self):
        super().setUp()
        self.hero = Hero.objects.create(
            name='hero_name',
            user=self.user,
        )
        self.main_statistic = HeroMainStatistic.objects.create(
            name='strength',
            value=10,
            hero=self.hero,
        )
        self.derivative_statistic = HeroDerivativeStatistic.objects.create(
            name='attack',
            multiplier=2,
            hero=self.hero,
            parent=self.main_statistic,
        )

    def test_statistic_string_representation(self):
        str_repr = "Hero derivative statistic " + self.derivative_statistic.name
        self.assertEqual(str(self.derivative_statistic), str_repr)

    def test_calculate_value(self):
        self.derivative_statistic.calculate_and_save_value()
        value = self.derivative_statistic.parent.value * self.derivative_statistic.multiplier
        self.assertEqual(self.derivative_statistic.value, value)


class TestItemMainStatistic(UserSetUp):
    def test_item_statistic_string_representation(self):
        hero = Hero.objects.create(
            user=self.user,
            name='hero'
        )
        item = Item.objects.create(
            owner=hero,
            name='item'
        )
        statistic_name = 'strength'
        item_statistic = ItemMainStatistic.objects.create(
            name=statistic_name,
            value=10,
            item=item
        )
        string_representation = 'Main statistic ' + statistic_name
        self.assertEqual(str(item_statistic), string_representation)