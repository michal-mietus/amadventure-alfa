from django.db import models
from .new_hero import NewHero


class NewItem(models.Model):
    name = models.CharField(max_length=20)
    owner = models.ForeignKey(NewHero, on_delete=models.CASCADE)
    
    def __str__(self):
        repr = "Item " + self.name
        return repr

