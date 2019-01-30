from django.db import models
from django.contrib.auth.models import User
from .models import Statistics
from django.db.models.signals import post_save
from django.dispatch import receiver


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


@receiver(post_save, sender=Hero)
def update_statistics(sender, instance, *args, **kwargs):
    # instead of saving instance use update
    remove_item_stats(instance)
    calculate_stats(instance)
    add_item_stats(instance)


# TODO reduce code in these functions
# this code is really ugly !
def remove_item_stats(instance):
    hero = Hero.objects.filter(pk=instance.pk)  # TODO why without index return queryset?
    for item in hero[0].item_set.all():
        hero.update(
            strength = hero[0].strength - item.strength,
            defense = hero[0].defense - item.defense,
            physical_attack = hero[0].physical_attack - item.physical_attack,
            intelligence = hero[0].intelligence - item.intelligence,
            magic_attack = hero[0].magic_attack - item.magic_attack,
            magic_resist = hero[0].magic_resist - item.magic_resist,
            agility = hero[0].agility - item.agility,
            dodge_chance = hero[0].dodge_chance - item.dodge_chance,
            critic_chance = hero[0].critic_chance - item.critic_chance,
            vitality = hero[0].vitality - item.vitality,
            health = hero[0].health - item.health,
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
    hero = Hero.objects.filter(pk=instance.pk)  # TODO why without index return queryset?
    for item in hero[0].item_set.all():
        hero.update(
            strength = hero[0].strength + item.strength,
            defense = hero[0].defense + item.defense,
            physical_attack = hero[0].physical_attack + item.physical_attack,
            intelligence = hero[0].intelligence + item.intelligence,
            magic_attack = hero[0].magic_attack + item.magic_attack,
            magic_resist = hero[0].magic_resist + item.magic_resist,
            agility = hero[0].agility + item.agility,
            dodge_chance = hero[0].dodge_chance + item.dodge_chance,
            critic_chance = hero[0].critic_chance + item.critic_chance,
            vitality = hero[0].vitality + item.vitality,
            health = hero[0].health + item.health,
        )
