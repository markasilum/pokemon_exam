from django.urls import path
from .views import PokemonIndexView,SearchPokemonView, FilterPokemonView, PokemonDetailView

urlpatterns = [

    path("", PokemonIndexView.as_view(), name="index"),
    path("search/", SearchPokemonView.as_view(), name="search"),
    path("filter/", FilterPokemonView.as_view(), name="filter"),
    path("<int:pk>/", PokemonDetailView.as_view(), name="pokemon_detail"),

]