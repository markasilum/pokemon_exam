from django.db import models

# Create your models here.
class Pokemon(models.Model):
    name = models.CharField(max_length=30)
    sprite = models.CharField(max_length=255)
    base_experience = models.IntegerField()
    height = models.IntegerField()
    weight = models.IntegerField()
    pokemon_stats = models.ManyToManyField('pokemons.PokemonStat', related_name="pokemons")
    species = models.ForeignKey("pokemons.Species", on_delete=models.CASCADE, related_name="pokemons", null=True)
    types = models.ManyToManyField('pokemons.Type', related_name="pokemons")
    held_items = models.ManyToManyField('pokemons.Item', related_name="pokemons")
    abilities = models.ManyToManyField('pokemons.Ability', related_name="pokemons")
    moves = models.ManyToManyField('pokemons.Move', related_name="pokemons")

    def __str__(self):
        return self.name
    
	
class PokemonStat(models.Model):
    base_stat = models.IntegerField()
    effort = models.IntegerField()
    stat = models.ForeignKey('pokemons.Stat',  on_delete=models.CASCADE, related_name="pokemons")

    def __str__(self):
        return str(self.stat)

# class PokemonType(models.Model):
#     slot = models.IntegerField()
#     type = models.ForeignKey("pokemons.Type", on_delete=models.CASCADE, related_name="pokemons")

#     def __str__(self):
#         return self.type

class Species(models.Model):
    name = models.CharField(max_length=30)
    evolves_from_species = models.ForeignKey('self', on_delete=models.CASCADE, related_name="evolves_to", null=True)

    def __str__(self):
        return self.name

class Ability(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Move(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
     
class Stat(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
            return self.name

class Item(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
            return self.name

class Type(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
            return self.name
