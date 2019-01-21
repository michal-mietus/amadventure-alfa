from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Statistics(models.Model):
    strength = models.IntegerField(default=0)
    defense = models.IntegerField(default=0)  # 1.0 * strength
    physical_attack = models.IntegerField(default=0)  # 3.0 * strength
    intelligence = models.IntegerField(default=0)
    magic_attack = models.IntegerField(default=0)  # 3.0 * intelligence
    magic_resist = models.IntegerField(default=0)  # 1.0 * intelligence
    agility = models.IntegerField(default=0)
    dodge_chance = models.FloatField(default=0)  # 0.005 * agility
    critic_chance = models.FloatField(default=0)  # 0.0025 * agility
    vitality = models.IntegerField(default=0)
    health = models.IntegerField(default=0)  # 5.0 * vitality

    class Meta:
        abstract = True


class Hero(Statistics):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=20)
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)
    
    def __str__(self):
        repr = "Hero " + self.name
        return repr


# TODO reduce code in these functions


# this code is really ugly !
def remove_item_stats(instance):
    hero = Hero.objects.get(pk=instance.pk)
    hero_to_update = Hero.objects.filter(pk=instance.pk)  # TODO why without index return queryset?
    for item in hero.item_set.all():
        hero_to_update.update(
            strength = hero.strength - item.strength,
            defense = hero.defense - item.defense,
            physical_attack = hero.physical_attack - item.physical_attack,
            intelligence = hero.intelligence - item.intelligence,
            magic_attack = hero.magic_attack - item.magic_attack,
            magic_resist = hero.magic_resist - item.magic_resist,
            agility = hero.agility - item.agility,
            dodge_chance = hero.dodge_chance - item.dodge_chance,
            critic_chance = hero.critic_chance - item.critic_chance,
            vitality = hero.vitality - item.vitality,
            health = hero.health - item.health,
        )


# this code is really ugly !
def add_item_stats(instance):
    hero = Hero.objects.get(pk=instance.pk)  # TODO why without index return queryset?
    hero_to_update = Hero.objects.filter(pk=instance.pk)
    for item in hero.item_set.all():
        hero_to_update.update(
            strength = hero.strength + item.strength,
            defense = hero.defense + item.defense,
            physical_attack = hero.physical_attack + item.physical_attack,
            intelligence = hero.intelligence + item.intelligence,
            magic_attack = hero.magic_attack + item.magic_attack,
            magic_resist = hero.magic_resist + item.magic_resist,
            agility = hero.agility + item.agility,
            dodge_chance = hero.dodge_chance + item.dodge_chance,
            critic_chance = hero.critic_chance + item.critic_chance,
            vitality = hero.vitality + item.vitality,
            health = hero.health + item.health,
        )


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
    remove_item_stats(instance)
    calculate_stats(instance)
    add_item_stats(instance)


class Item(Statistics):
    name = models.CharField(max_length=20)
    owner = models.ForeignKey(Hero, on_delete=models.CASCADE)
    
    def __str__(self):
        repr = "Item " + self.name
        return repr


class Location(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return "Location " + self.name


class Action(models.Model):
    name = models.CharField(max_length=50)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return "Action " + self.name
