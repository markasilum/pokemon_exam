from django import forms
from django.forms import ModelForm
from pokemons.models import Pokemon, PokemonStat, Ability, Stat, Item, Type, Move, Species

class PokemonForm(ModelForm):
    class Meta:
        model = Pokemon
        fields = "__all__"