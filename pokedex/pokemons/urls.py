from django.urls import path
from .views import PokemonIndexView,SearchPokemonView

urlpatterns = [

    path("", PokemonIndexView.as_view(), name="index"),
    path("search/", SearchPokemonView.as_view(), name="search"),

]