from django import forms
from django.forms import ModelForm
from pokemons.models import Pokemon, PokemonStat, Ability, Stat, Item, Type, Move, Species
from django.forms import modelformset_factory
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

class PokemonForm(ModelForm):
    class Meta:
        model = Pokemon
        exclude = ['pokemon_stats']

class PokemonStatForm(forms.ModelForm):
    stat = forms.ModelChoiceField(queryset=Stat.objects.all(), disabled=True)

    class Meta:
        model = PokemonStat
        fields = ['stat', 'base_stat', 'effort']

PokemonStatFormSet = modelformset_factory(PokemonStat, form=PokemonStatForm, extra=0)


class PokemonTypeFilterForm(forms.Form):
    type = forms.ModelChoiceField(queryset=Type.objects.all(), required=True, empty_label="Choose a Type")

class PokemonFilterForm(forms.Form):
    type = forms.ModelChoiceField(queryset=Type.objects.all(), required=False, empty_label="Select a type")

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]
