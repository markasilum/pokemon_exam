from django import forms
from django.forms import ModelForm
from pokemons.models import Pokemon, PokemonStat, Ability, Stat, Item, Type, Move, Species

class PokemonForm(ModelForm):
    class Meta:
        model = Pokemon
        fields = "__all__"

class PokemonTypeFilterForm(forms.Form):
    type = forms.ModelChoiceField(queryset=Type.objects.all(), required=True, empty_label="Choose a Type")

class PokemonFilterForm(forms.Form):
    type = forms.ModelChoiceField(queryset=Type.objects.all(), required=False, empty_label="Select a type")
