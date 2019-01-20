from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Statistics(models.Model):
    strength = models.IntegerField()
    defense = models.IntegerField(default=0)  # 1.0 * strength
    physical_attack = models.IntegerField(default=0)  # 3.0 * strength
    intelligence = models.IntegerField()
    magic_attack = models.IntegerField(default=0)  # 3.0 * intelligence
    magic_resist = models.IntegerField(default=0)  # 1.0 * intelligence
    agility = models.IntegerField()
    dodge_chance = models.FloatField(default=0)  # 0.005 * agility
    critic_chance = models.FloatField(default=0)  # 0.0025 * agility
    vitality = models.IntegerField()
    health = models.IntegerField(default=0)  # 5.0 * vitality

    class Meta:
        abstract = True


class Hero(Statistics):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=20)
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)
    
    def __str__(self):
        return "Hero " + self.name
 

    def remove_item_stats(self):
        """Removes all bonuses getted from items"""
        for item in self.item_set.all():
            self.strength -= item.strength
            self.intelligence -= item.intelligence
            self.agility -= item.agility
            self.vitality -= item.agility

    def add_item_stats(self):
        """Adds all bonuses getted from items"""
        for item in self.item_set.all():
            self.strength += item.strength
            self.intelligence += item.intelligence
            self.agility += item.agility
            self.vitality += item.agility


def add_item_stats():
    hero = Hero.objects.all()
    #for item in


def calculate_stats(instance):
    hero = Hero.objects.filter(pk=instance.pk)
    hero.update(
        defense = instance.strength * 1.0,
        physical_attack = instance.strength * 3.0,
        magic_attack = instance.intelligence * 3.0,
        magic_resist = instance.intelligence * 1.0,
        dodge_chance = instance.agility * 0.0025,
        critic_chance = instance.agility * 0.005,
        health = instance.vitality * 5,
    )

@receiver(post_save, sender=Hero)
def update_statistics(sender, instance, *args, **kwargs):
    # instead of saving instance use update
    calculate_stats(instance)


class Item(Statistics):
    name = models.CharField(max_length=20)
    owner = models.ForeignKey(Hero, on_delete=models.CASCADE)
    
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
