from django.db import models
from .hero import Hero


class Item(models.Model):
    name = models.CharField(max_length=20)
    owner = models.ForeignKey(Hero, on_delete=models.CASCADE)
    
    def __str__(self):
        repr = "Item " + self.name
        return repr

    def get_all_statistics(self):
        return self.itemstatistic_set.all()

