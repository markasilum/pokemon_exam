from django.contrib import admin
from .models import Pokemon, PokemonStat, Species, Ability, Move, Stat, Item, Type

@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_experience', 'height', 'weight', 'species')
    search_fields = ('name',)
    list_filter = ('species', 'types')
    filter_horizontal = ('pokemon_stats', 'types', 'held_items', 'abilities', 'moves')

@admin.register(PokemonStat)
class PokemonStatAdmin(admin.ModelAdmin):
    list_display = ('stat', 'base_stat', 'effort')
    search_fields = ('stat__name',)
    list_filter = ('stat',)

@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('name', 'evolves_from_species')
    search_fields = ('name',)

@admin.register(Ability)
class AbilityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Move)
class MoveAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
