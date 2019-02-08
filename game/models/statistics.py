from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .hero import Hero
from .item import Item


class MainStatistic(models.Model):
    name = models.CharField(max_length=20)
    value = models.PositiveIntegerField()

    class Meta:
        abstract = True

    def __str__(self):
        str = "Main statistic " + self.name
        return str


class HeroMainStatistic(MainStatistic):
    hero = models.ForeignKey(Hero, on_delete=models.CASCADE)

    def get_all_derivative_statistics(self):
        return self.heroderivativestatistic_set.all()


class ItemMainStatistic(MainStatistic):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)


class DerivativeStatistic(models.Model):
    """ Derivative statistics from MainStatistics """

    name = models.CharField(max_length=20)
    value = models.FloatField(default=1)
    multiplier = models.FloatField(default=1)

    class Meta:
        abstract = True

    def __str__(self):
        str = "Hero derivative statistic " + self.name
        return str

    def calculate_and_save_value(self):
        if self.parent:
            self.value = self.parent.value * self.multiplier
            self.save()


class HeroDerivativeStatistic(DerivativeStatistic):
    hero = models.ForeignKey(Hero, on_delete=models.CASCADE)
    parent = models.ForeignKey(HeroMainStatistic, on_delete=models.CASCADE)


class ItemDerivativeStatistic(DerivativeStatistic):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    parent = models.ForeignKey(ItemMainStatistic, on_delete=models.CASCADE)
