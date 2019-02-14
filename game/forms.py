from django import forms
from .models.hero import Hero


class HeroForm(forms.ModelForm):
    class Meta:
        model = Hero
        fields = ['name']


class HeroDeleteForm(forms.Form):
    hero_name = forms.CharField(max_length=20)


class MainStatisticsForm(forms.Form):
    strength = forms.IntegerField(min_value=1)
    intelligence = forms.IntegerField(min_value=1)
    agility = forms.IntegerField(min_value=1)
    vitality = forms.IntegerField(min_value=1)
