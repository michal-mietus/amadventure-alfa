from django.db import models
from .hero import Hero
from .models import Statistics



class Item(Statistics):
    name = models.CharField(max_length=20)
    owner = models.ForeignKey(Hero, on_delete=models.CASCADE)
    
    def __str__(self):
        repr = "Item " + self.name
        return repr

