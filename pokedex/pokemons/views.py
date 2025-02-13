from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView, FormView

from pokemons.models import Pokemon, PokemonStat, Ability, Stat, Item, Type, Move, Species
from .forms import PokemonForm, PokemonTypeFilterForm,PokemonFilterForm
# Create your views here.
class PokemonIndexView(ListView):
    model = Pokemon
    context_object_name = "pokemons"
    template_name = "index.html" 
    
    def get_queryset(self):
        return Pokemon.objects.all().order_by("name")

class PokemonListView(ListView):
    """Handles both searching and filtering Pokémon."""

    template_name = 'index.html'

    def get(self, request):
        query = request.GET.get('query', '')
        form = PokemonFilterForm()  # Always visible

        if query:
            pokemons = Pokemon.objects.filter(name__icontains=query)
            mode = "search"
        else:
            pokemons = Pokemon.objects.all()
            mode = "index"

        context = {
            'pokemons': pokemons,
            'query': query,
            'form_type': form,
            'mode': mode,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = PokemonFilterForm(request.POST)

        if form.is_valid() and form.cleaned_data['type']:
            selected_type = form.cleaned_data['type']
            pokemons = Pokemon.objects.filter(types=selected_type)
            mode = "filter"
        else:
            pokemons = Pokemon.objects.all()
            mode = "index"

        context = {
            'pokemons': pokemons,
            'form_type': form,
            'mode': mode,
        }
        return render(request, self.template_name, context)
    
# class SearchPokemonView(ListView):
#     model = Pokemon
#     context_object_name = "pokemon_search"
#     template_name = 'index.html'

#     def get(self, request):
#         query = request.GET.get('query', '')

#         if query:
#             pokemons = Pokemon.objects.filter(name__icontains=query)
#             mode = "search"
#         else:
#             pokemons = Pokemon.objects.all()
#             mode = "index"

#         context = {
#             'pokemons': pokemons,
#             'query': query,
#             'form_type': PokemonFilterForm(),
#             'mode': mode,
#         }
#         return render(request, self.template_name, context)
    
# class FilterPokemonView(ListView):
#     template_name = 'index.html'  # Update with the correct path to your template
#     def post(self, request):
#         form = PokemonFilterForm(request.POST)

#         if form.is_valid():
#             selected_type = form.cleaned_data['type']
#             pokemons = Pokemon.objects.filter(types=selected_type)
#             mode = "filter"
#         else:
#             pokemons = Pokemon.objects.all()
#             mode = "index"

#         context = {
#             'pokemons': pokemons,
#             'form_type': form,
#             'mode': mode,
#         }
#         return render(request, self.template_name, context)
    
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
    
class CreatePokemonView(CreateView):
    model = Pokemon
    form_class = PokemonForm
    template_name = "create_pokemon.html"
    success_url = reverse_lazy("index")


class DeletePokemonView(DeleteView):
    model = Pokemon
    template_name = "delete_pokemon.html"
    success_url = reverse_lazy("index")

class UpdatePokemonView(UpdateView):
    model = Pokemon
    form_class = PokemonForm
    template_name = "update_pokemon.html"
    success_url = reverse_lazy("index")

def pokemon_filter_view(request):
    pokemons = Pokemon.objects.all()  # Default to showing all Pokémon

    # Process form submission
    if request.method == 'POST':
        form = PokemonFilterForm(request.POST)
        if form.is_valid():
            selected_type = form.cleaned_data['type']
            # Filter Pokémon based on the selected type
            pokemons = Pokemon.objects.filter(types=selected_type)
    else:
        form = PokemonFilterForm()

    # Pass filtered Pokémon and form to the template
    context = {
        'form_type': form,
        'pokemons': pokemons,
    }
    return render(request, 'index.html', context)