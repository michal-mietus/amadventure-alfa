from django.db import models


class Hero(models.model):
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
        return self.name
