from ...models.statistic import Statistic
from ...models.hero import Hero
from .set_ups import UserSetUp


class TestStatistic(UserSetUp):
    def setUp(self):
        super().setUp()
        self.statistic = Statistic.objects.create(
            name='strength',
            multiplier=1,
            value=10,
        )

    def test_statistic_string_representation(self):
        str_repr = "Statistic " + self.statistic.name
        self.assertEqual(str(self.statistic), str_repr)

    def test_create_statistics(self):
        statistics_pairs = {
            'Strength': 10,
            'Intelligence': 5,
            'Agility': 7,
            'Vitality': 6,
        }
        for name, value in statistics_pairs.items():
            Statistic.objects.create(
                name=name,
                value=value,
            )

    def test_create_child_statistic(self):
        child_statistic = Statistic.objects.create(
            name='defense',
            parent=self.statistic,
            multiplier=3,
            value=10,
        )

    def test_calculate_value(self):
        value=10
        multiplier=3
        child_statistic = Statistic.objects.create(
            name='defense',
            parent=self.statistic,
            multiplier=multiplier,
            value=value,
        )
        child_statistic.calculate_value()
        self.assertEqual(child_statistic.value, value*multiplier)

