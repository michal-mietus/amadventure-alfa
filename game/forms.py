from django.forms import ModelForm
from .models.hero import Hero


class HeroCreateForm(ModelForm):
    class Meta:
        model = Hero
        fields = ['name', 'strength', 'intelligence', 'agility', 'vitality']


class HeroUpgradeForm(ModelForm):
    class Meta:
        model = Hero
        fields = ['strength', 'intelligence', 'agility', 'vitality']
