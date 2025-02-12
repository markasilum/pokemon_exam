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
    
class FilterPokemonView(ListView):
    model = Pokemon
    context_object_name = "pokemon_filter"
    template_name = 'index.html'

    def get_queryset(self):
        type_filter = self.request.GET.get("type", "")  # Get the selected type filter
        
        if type_filter:
            result = Pokemon.objects.filter(types__name=type_filter)  # Filter by type
        else:
            result = Pokemon.objects.all()  # If no type filter, return all Pokémon

        return result
    
class PokemonDetailView(DetailView):
    model = Pokemon
    context_object_name = "pokemon"
    template_name = "pokemon_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pokemon_stats"] = self.object.pokemon_stats.all()  # Fetch related stats

        species = self.object.species  # Get Pokémon's species

        # Previous evolution (if exists)
        context["previous_evolution"] = species.evolves_from_species if species else None  

        # Next evolutions (if exists)
        context["next_evolutions"] = species.evolves_to.all() if species else []  

        return context
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["books"] =(self.object.books.all())
    #     return context