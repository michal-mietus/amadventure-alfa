from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator


class Statistics(models.Model):
    strength = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1)])
    defense = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1)])  # 0.5 * strength
    physical_attack = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1)])  # 1.5 * strength
    intelligence = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1)])
    magic_attack = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1)])  # 1.5 * intelligence
    magic_resist = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1)])  # 0.5 * intelligence
    agility = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1)])
    dodge_chance = models.FloatField(default=0)  # 0.005 * agility
    critic_chance = models.FloatField(default=0)  # 0.0025 * agility
    vitality = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1)])
    health = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1)])  # 5.0 * vitality

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
    
    def fight(self, enemy):
        attacker = Fighter(self, enemy)
        defender = Fighter(enemy, self)

        while (attacker.health and defender.health) > 0:
            attacker.hit(defender)
            defender.hit(attacker)
        
        return self.choose_winner(attacker, defender)
        
    def choose_winner(self, attacker, defender):
        if attacker.health > defender.health:
            str = "Attacker won"
        else:
            str = "Defender won"
        return str


class Fighter:
    def __init__(self, hero, enemy):
        self.health = hero.health
        self.physical_damage = self.calculate_physical_damage(hero, enemy)
        self.magical_damage = self.calculate_magical_damage(hero, enemy)

    def hit_enemy(self, enemy):
        enemy.health -= self.physical_damage + self.magical_damage

    def calculate_physical_damage(self, hero, enemy):
        physical_damage = hero.physical_attack / enemy.defense
        return physical_damage

    def calculate_magical_damage(self, hero, enemy):
        magical_damage = hero.magic_attack / enemy.magic_resist
        return magical_damage



@receiver(post_save, sender=Hero)
def update_statistics(sender, instance, *args, **kwargs):
    # instead of saving instance use update
    remove_item_stats(instance)
    calculate_stats(instance)
    add_item_stats(instance)


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


def calculate_stats(instance):
    hero = Hero.objects.filter(pk=instance.pk)
    hero.update(
        defense = instance.strength * 0.5,
        physical_attack = instance.strength * 1.5,
        magic_attack = instance.intelligence * 1.5,
        magic_resist = instance.intelligence * 0.5,
        dodge_chance = instance.agility * 0.0025,
        critic_chance = instance.agility * 0.005,
        health = instance.vitality * 5,
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
