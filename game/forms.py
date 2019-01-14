from django.forms import ModelForm
from . import models


class HeroForm(ModelForm):
    class Meta:
        model = models.Hero
        exclude = [
            'user', 'level', 'experience',
            'dodge_chance', 'critic_chance'
            ]

    field_order = ['name', 'strength', 'intelligence', 'agility', 'health']