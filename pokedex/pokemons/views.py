from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from pokemons.models import Pokemon, PokemonStat, Ability, Stat, Item, Type, Move, Species
from .forms import PokemonForm, PokemonTypeFilterForm,PokemonFilterForm, PokemonStatForm, PokemonStatFormSet,LoginForm, CreateUserForm

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
            pokemons = Pokemon.objects.filter(name__icontains=query).order_by('name')
            mode = "search"
        else:
            pokemons = Pokemon.objects.all().order_by('name')
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
            pokemons = Pokemon.objects.all().order_by('name')
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

        # Previous evolution (if exists in the database)
        if species:
            previous_evolution = species.evolves_from_species
            # print(previous_evolution.id)
           
            if previous_evolution:
                if not Pokemon.objects.filter(species_id=previous_evolution.id).exists():
                    context["previous_evolution"] = "This Pokémon is not in the database."
                else:
                    pokemon = Pokemon.objects.get(species_id=previous_evolution.id)
                    context["previous_evolution"] = pokemon
            else:
                context["previous_evolution"] = None
        else:
            context["previous_evolution"] = None

        # Next evolutions (if exists in the database)
        if species:
            next_evolutions = species.evolves_to.all()
            valid_next_evolutions = []
            for evolution in next_evolutions:
                if not Species.objects.filter(id=evolution.id).exists():
                    valid_next_evolutions.append("This Pokémon is not in the database.")
                else:
                    valid_next_evolutions.append(evolution)
            context["next_evolutions"] = valid_next_evolutions
        else:
            context["next_evolutions"] = []

        return context
    
class CreatePokemonView(LoginRequiredMixin, CreateView):
    model = Pokemon
    form_class = PokemonForm
    template_name = "create_pokemon.html"
    success_url = reverse_lazy("index")


class DeletePokemonView(LoginRequiredMixin, DeleteView):
    model = Pokemon
    template_name = "delete_pokemon.html"
    success_url = reverse_lazy("index")

class UpdatePokemonView(LoginRequiredMixin, UpdateView):
    model = Pokemon
    form_class = PokemonForm
    template_name = "update_pokemon.html"
    success_url = reverse_lazy("index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pokemon = self.object

        # Create a formset for the Pokémon's stats
        formset = PokemonStatFormSet(queryset=PokemonStat.objects.filter(pokemons=pokemon))

        context['formset'] = formset
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = PokemonStatFormSet(request.POST, queryset=PokemonStat.objects.filter(pokemon=self.object))

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()  # This updates the PokemonStat records correctly
            return redirect(self.success_url)

        return self.render_to_response(self.get_context_data(form=form, formset=formset))

