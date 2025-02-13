from django.urls import path
from .views import (
    PokemonIndexView,
    PokemonDetailView,
    CreatePokemonView,
    UpdatePokemonView,
    DeletePokemonView,
    PokemonListView
    # pokemon_filter_view,
    # SearchPokemonView, 
    # FilterPokemonView,
)

urlpatterns = [
    path("", PokemonListView.as_view(), name="index"),
    # path("search/", SearchPokemonView.as_view(), name="search"),
    # path("filter/", FilterPokemonView.as_view(), name="filter"),
    path("pokemon/<int:pk>/", PokemonDetailView.as_view(), name="pokemon_detail"),
    path("pokemon/create/", CreatePokemonView.as_view(), name="create_pokemon"),
    path("pokemon/<int:pk>/update", UpdatePokemonView.as_view(), name="update_pokemon"),
    path("pokemon/<int:pk>/delete", DeletePokemonView.as_view(), name="delete_pokemon"),
    # path('filter/', pokemon_filter_view, name='filter'),
]
