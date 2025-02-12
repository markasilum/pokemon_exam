import requests
from django.core.management.base import BaseCommand
from pokemons.models import Pokemon, PokemonStat, Species, Ability, Move, Stat, Item, Type


class Command(BaseCommand):
    help = "Example command with an optional --delete argument"

    def handle(self, *args, **options):
        pokemon = Pokemon.objects.all().delete()
        pokemon_stat = PokemonStat.objects.all().delete()
        species = Species.objects.all().delete()
        ability = Ability.objects.all().delete()
        move = Move.objects.all().delete()
        stat = Stat.objects.all().delete()
        item = Item.objects.all().delete()
        type = Type.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleared records from database'))