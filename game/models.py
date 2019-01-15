from django.db import models
from django.contrib.auth.models import User


class Statistics(models.Model):
    strength = models.IntegerField()
    intelligence = models.IntegerField()
    agility = models.IntegerField()
    dodge_chance = models.IntegerField(default=0)
    critic_chance = models.IntegerField(default=0)
    health = models.IntegerField(default=0)

    class Meta:
        abstract = True
 

class Hero(Statistics):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)
    health = models.IntegerField(default=10)
    
    def __str__(self):
        return "Hero " + self.name


class Item(Statistics):
    name = models.CharField(max_length=20)
    minimal_level = models.IntegerField()
    
    def __str__(self):
        return "Item " + self.name


class Location(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return "Location " + self.name


class Action(models.Model):
    name = models.CharField(max_length=50)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return "Action " + self.name
