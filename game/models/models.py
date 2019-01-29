from django.db import models
from django.contrib.auth.models import User
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
