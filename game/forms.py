from django import forms
from .models.hero import Hero
from .models.statistic import HeroStatistic


class HeroForm(forms.ModelForm):
    class Meta:
        model = Hero
        fields = ['name']


class HeroStatisticsForm(forms.Form):
    strength = forms.IntegerField(min_value=1)
    intelligence = forms.IntegerField(min_value=1)
    agility = forms.IntegerField(min_value=1)
    vitality = forms.IntegerField(min_value=1)
