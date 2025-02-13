from django import forms
from django.forms import ModelForm
from pokemons.models import Pokemon, PokemonStat, Ability, Stat, Item, Type, Move, Species
from django.forms import modelformset_factory

class PokemonForm(ModelForm):
    class Meta:
        model = Pokemon
        exclude = ['pokemon_stats']  # Exclude Many-to-Many with extra fields

class PokemonStatForm(forms.ModelForm):
    stat = forms.ModelChoiceField(queryset=Stat.objects.all(), disabled=True)  # Prevent changing existing stats

    class Meta:
        model = PokemonStat
        fields = ['stat', 'base_stat', 'effort']

PokemonStatFormSet = modelformset_factory(PokemonStat, form=PokemonStatForm, extra=0)  # No extra empty forms


class PokemonTypeFilterForm(forms.Form):
    type = forms.ModelChoiceField(queryset=Type.objects.all(), required=True, empty_label="Choose a Type")

class PokemonFilterForm(forms.Form):
    type = forms.ModelChoiceField(queryset=Type.objects.all(), required=False, empty_label="Select a type")
