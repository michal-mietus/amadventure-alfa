from django.db import models
from .hero import Hero
from itertools import chain


class Item(models.Model):
    name = models.CharField(max_length=20)
    # TODO this item can assign only to hero!
    owner = models.ForeignKey(Hero, on_delete=models.CASCADE)
    
    def __str__(self):
        repr = "Item " + self.name
        return repr

    def get_all_list_statistics(self):
        statistics = list(chain(self.itemmainstatistic_set.all(), self.itemderivativestatistic_set.all()))
        return statistics

