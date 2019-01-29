from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .hero import Hero
from .item import Item


class Statistic(models.Model):
    name = models.CharField(max_length=20)
    parent = models.ForeignKey('self', null=True, default=None, on_delete=models.CASCADE)
    multiplier = models.FloatField(default=1)
    value = models.PositiveIntegerField()

    def __str__(self):
        str = "Statistic " + self.name
        return str

    def calculate_value(self):
        if self.parent:
            self.value = self.parent.value * self.multiplier


class HeroStatistics(Statistic):
    owner = models.ForeignKey(Hero, on_delete=models.CASCADE)


class ItemStatistics(Statistic):
    owner = models.ForeignKey(Item, on_delete=models.CASCADE)
