from django.forms import ModelForm
from . import models


class HeroCreateForm(ModelForm):
    class Meta:
        model = models.Hero
        fields = ['name', 'strength', 'intelligence', 'agility', 'vitality']


class HeroUpgradeForm(ModelForm):
    class Meta:
        model = models.Hero
        fields = ['strength', 'intelligence', 'agility', 'vitality']
