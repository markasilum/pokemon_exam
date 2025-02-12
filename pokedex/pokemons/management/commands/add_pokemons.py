import requests
from django.core.management.base import BaseCommand
from pokemons.models import Pokemon, PokemonStat, Ability, Stat, Item, Type, Move, Species

class Command(BaseCommand):
    """Add pokemon command Version 1.0"""
    help = "Example command with an optional --delete argument"

    def handle(self, *args, **options):
        generation_one_api = requests.get('https://pokeapi.co/api/v2/generation/1/')
        json_data = generation_one_api.json()
        
        pokemon_species = json_data["pokemon_species"]
        moves = json_data["moves"]
        types = json_data["types"]

        
        """Done for now"""
        for move in moves:
            name = move['name']
            move = Move(name=name)
            move.save()

        for type in types:
            name = type['name']
            type = Type(name=name)
            type.save()

        """For adding pokemons"""
        for species in pokemon_species:
            url = species['url']
            response = requests.get(url)
            
            if response.status_code != 200:
                print(f"Failed to fetch data for {url}")
                continue

            species_data = response.json()
            species_name = species_data['name']
            evolves_from = species_data.get('evolves_from_species')  # Use .get() to avoid KeyError

            # Check if the species already exists in the database
            species_instance, created = Species.objects.get_or_create(name=species_name)

            if evolves_from:
                parent_name = evolves_from['name']
                parent_species = Species.objects.filter(name=parent_name).first()

                if parent_species:
                    species_instance.evolves_from_species = parent_species
                    print(f"Connected {species_name} to existing species {parent_name}")
                else:
                    future_species = Species.objects.create(name=parent_name)
                    species_instance.evolves_from_species = future_species
                    print(f"Created and connected {species_name} to newly added species {parent_name}")

            species_instance.save()
            print(f"Saved {species_name} successfully.")


            

        self.stdout.write(self.style.SUCCESS('Successfully added pokemons to database'))