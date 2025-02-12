import requests
from django.core.management.base import BaseCommand
from pokemons.models import Pokemon, PokemonStat, Ability, Stat, Item, Type, Move, Species

class Command(BaseCommand):
    """Add pokemon command Version 2.0"""

    help = "Example command with an optional --delete argument"

    def handle(self, *args, **options):
        generation_one_api = requests.get('https://pokeapi.co/api/v2/pokemon/?limit=6&offset=146')
        json_data = generation_one_api.json()
        
        pokemons = json_data["results"]

        for pokemon in pokemons:
            pokemon_name = pokemon["name"]
            pokemon_detail_url = pokemon['url']

            pokemon_detail_response = requests.get(pokemon_detail_url)
            pokemon_detail_json = pokemon_detail_response.json()

            base_experience = pokemon_detail_json['base_experience']
            height = pokemon_detail_json['height']
            weight = pokemon_detail_json['weight']
            sprites = pokemon_detail_json['sprites']['front_default']

            #parsing and creating abilites
            ability_list = pokemon_detail_json.get('abilities', [])
            ability_instances = []
            if ability_list:
                for ability in ability_list:
                    ability_name = ability['ability']['name']
                    ability_instance, created = Ability.objects.get_or_create(name=ability_name)
                    ability_instances.append(ability_instance)


            held_items_list = pokemon_detail_json.get('held_items',[])
            item_instances = []
            if held_items_list:
                for item in held_items_list:
                    item_name = item['item']['name']
                    item_instance, created = Item.objects.get_or_create(name=item_name)
                    item_instances.append(item_instance)

            moves_list = pokemon_detail_json.get('moves',[])
            move_instances = []
            if moves_list:
                for move in moves_list:
                    move_name = move['move']['name']
                    move_instance, created = Move.objects.get_or_create(name=move_name)
                    move_instances.append(move_instance)
            
            stat_list = pokemon_detail_json.get('stats',[])
            pokemon_stat = []  # This should store model instances, not dictionaries

            for stat in stat_list:
                base_stat = stat['base_stat']
                effort = stat['effort']
                stat_name = stat['stat']['name']

                # Fetch or create the stat in the database
                stat_instance, _ = Stat.objects.get_or_create(name=stat_name)

                # Create a PokemonStat instance (do not commit yet)
                pokemon_stat_obj = PokemonStat.objects.create(
                    base_stat=base_stat,
                    effort=effort,
                    stat=stat_instance  # Pass the actual instance, not just the ID
                )

                # Append PokemonStat instance (not a dictionary)
                pokemon_stat.append(pokemon_stat_obj)
            
            types = pokemon_detail_json.get('types',[])
            type_instances = []
            if types:
                for type in types:
                    type_name = type['type']['name']
                    type_instance, created = Type.objects.get_or_create(name=type_name)
                    type_instances.append(type_instance)
            
            #loop here
            species_name = pokemon_detail_json['species']['name']
            species_url = pokemon_detail_json['species']['url']

            species_url_response = requests.get(species_url)
            species_data = species_url_response.json()

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

            existing_pokemon = Pokemon.objects.filter(name=pokemon_name).first()

            if existing_pokemon:
                print(f"Pokémon '{pokemon_name}' already exists.")
            else:
                create_pokemon = Pokemon(
                    name=pokemon_name,
                    sprite=sprites,
                    height=height,
                    weight=weight,
                    base_experience=base_experience,
                    species = species_instance
                    )
                create_pokemon.save()

                create_pokemon.pokemon_stats.add(*pokemon_stat)
                create_pokemon.types.add(*type_instances)
                create_pokemon.abilities.add(*ability_instances)
                create_pokemon.held_items.add(*item_instances)
                create_pokemon.moves.add(*move_instances)

                self.stdout.write(self.style.SUCCESS(f"{pokemon_name} was added to the database"))





            """ 
            sprite = models.CharField(max_length=255)
            base_experience = models.IntegerField()
            height = models.IntegerField()
            weight = models.IntegerField()
            pokemon_stats = models.ManyToManyField('pokemons.PokemonStat', related_name="pokemons", null=True)
            species = models.ForeignKey("pokemons.Species", on_delete=models.CASCADE, related_name="pokemons", null=True)
            types = models.ManyToManyField('pokemons.PokemonType', related_name="pokemons", null=True)
            held_items = models.ManyToManyField('pokemons.Item', related_name="pokemons", null=True)
            abilities = models.ManyToManyField('pokemons.Ability', related_name="pokemons", null=True)
            """



