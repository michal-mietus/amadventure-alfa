from django.db import models
from django.contrib.auth.models import User


class Hero(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField()
    level = models.IntegerField()
    experience = models.IntegerField()
    strength = models.IntegerField()
    intelligence = models.IntegerField()
    agility = models.IntegerField()
    dodge_chance = models.IntegerField()
    critic_chance = models.IntegerField()
    health = models.IntegerField()

    def __str__(self);
        return "Hero " + self.name


class Location(models.Model):
    name = models.CharField()
    
    def __str__(self);
        return "Location " + self.name


class Action(models.Model):
    name = models.CharField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self);
        return "Action " + self.name
