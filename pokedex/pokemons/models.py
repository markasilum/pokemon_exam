from django.db import models

# Create your models here.
class Pokemon(models.Model):
    name = models.CharField(max_length=30)
    sprite = models.CharField(max_length=255)
    base_experience = models.IntegerField()
    height = models.IntegerField()
    weight = models.IntegerField()
    pokemon_stats = models.ManyToManyField('pokemons.PokemonStat', related_name="pokemons", null=True)
    species = models.ForeignKey("pokemons.Species", on_delete=models.CASCADE, related_name="pokemons")
    types = models.ManyToManyField('pokemons.PokemonType', related_name="pokemons", null=True)
    held_items = models.ManyToManyField('pokemons.Item', related_name="pokemons", null=True)
	
class PokemonStat(models.Model):
    base_stat = models.IntegerField()
    effort = models.IntegerField()
    stat = models.ForeignKey('pokemons.Stat',  on_delete=models.CASCADE, related_name="pokemons")

class PokemonType(models.Model):
    slot = models.IntegerField()
    type = models.ForeignKey("pokemons.Type", on_delete=models.CASCADE, related_name="pokemons")

class Species(models.Model):
    name = models.CharField(max_length=30)

class Ability(models.Model):
    name = models.CharField(max_length=30)

class Move(models.Model):
	name = models.CharField(max_length=30)

class Stat(models.Model):
	name = models.CharField(max_length=30)

class Item(models.Model):
	name = models.CharField(max_length=30)

class Type(models.Model):
	name = models.CharField(max_length=30)
