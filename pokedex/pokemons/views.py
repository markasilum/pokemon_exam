from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from pokemons.models import Pokemon, PokemonStat, Ability, Stat, Item, Type, Move, Species

# Create your views here.
class PokemonIndexView(ListView):
    model = Pokemon
    context_object_name = "pokemons"
    template_name = "index.html" 
    
    def get_queryset(self):
        return Pokemon.objects.all().order_by("name")
    
class SearchPokemonView(ListView):
    model = Pokemon
    context_object_name = "pokemon_search"
    template_name = 'index.html'

    def get_queryset(self):
        query = self.request.GET.get("query", "")
        if query:
            result = Pokemon.objects.filter(name__icontains=query)
            print(result)
            return result  # Filter by Pokemon name
        return Pokemon.objects.all()
    