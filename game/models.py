from django.db import models
from django.contrib.auth.models import User


class Hero(Statistics):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    level = models.IntegerField()
    experience = models.IntegerField()
    
    def __str__(self):
        return "Hero " + self.name


class Location(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return "Location " + self.name


class Action(models.Model):
    name = models.CharField(max_length=50)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return "Action " + self.name


class Item(Statistics):
    name = models.CharField(max_length=20)
    minimal_level = models.IntegerField()


class Statistics(models.Model):
    strength = models.IntegerField()
    intelligence = models.IntegerField()
    agility = models.IntegerField()
    dodge_chance = models.IntegerField()
    critic_chance = models.IntegerField()
    health = models.IntegerField()

    class Meta:
        abstract = True
 