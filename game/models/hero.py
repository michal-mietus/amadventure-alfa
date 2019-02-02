from django.db import models
from django.contrib.auth.models import User


class Hero(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    
    def __str__(self):
        repr = "Hero " + self.name
        return repr

    def get_statistic(self, name):
        return self.herostatistic_set.get(name=name)

    def get_all_statistics(self):
        return self.herostatistic_set.all()

    def get_all_items(self):
        return self.item_set.all()

    def remove_items_statistics(self):
        for item in self.get_all_items():
            for item_statistic in item.get_all_statistics():
                self.remove_item_statistic(item_statistic)

    def add_item_statistics(self):
        for item in self.get_all_items():
            for item_statistic in item.get_all_statistics():
                self.add_item_statistic(item_statistic)
                
    def remove_item_statistic(self, item_statistic):
        hero_statistic = self.get_statistic(item_statistic.name)
        hero_statistic.value -= item_statistic.value
        hero_statistic.save()

    def add_item_statistic(self, item_statistic):
        hero_statistic = self.get_statistic(item_statistic.name)
        hero_statistic.value += item_statistic.value
        hero_statistic.save()

    # TODO create method to calcualte stats without items
    # TODO remove and add item stats 
