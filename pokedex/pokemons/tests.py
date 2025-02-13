from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Pokemon, PokemonStat, Stat, Species, Type, Item, Ability, Move
from django.contrib.auth.models import User


class CreatePokemonViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a user for login
        cls.user = User.objects.create_user(username="testuser", password="testpassword")
        
        # Create related objects (Stat, PokemonStat, Species, Type, Item, Ability, Move)
        cls.stat = Stat.objects.create(name="Speed")
        cls.pokemon_stat = PokemonStat.objects.create(base_stat=60, effort=2, stat=cls.stat)
        
        cls.species = Species.objects.create(name="Electric Mouse")
        cls.type = Type.objects.create(name="Electric")
        cls.item = Item.objects.create(name="Thunder Stone")
        cls.ability = Ability.objects.create(name="Static")
        cls.move = Move.objects.create(name="Thunderbolt")
        
    def setUp(self):
        # Log in the user before each test
        self.client.login(username="testuser", password="testpassword")
        
    def test_create_pokemon_view_get(self):
        """
        Test if the 'CreatePokemonView' returns a valid response when accessing via GET.
        """
        url = reverse("create_pokemon")  # Adjust this URL name based on your urls.py
        response = self.client.get(url)
        
        # Check if the response status is 200 OK (valid response)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "create_pokemon.html")  # Ensure the correct template is used
        
        # Ensure the form is present in the context
        self.assertIn("form", response.context)
    
    def test_create_pokemon_view_post_valid(self):
        """
        Test if a valid POST request to create a Pokémon redirects to the correct success URL.
        """
        url = reverse("create_pokemon")  # Adjust this URL name based on your urls.py
        data = {
            "name": "Pikachu",
            "sprite": "pikachu_sprite_url",
            "base_experience": 112,
            "height": 4,
            "weight": 60,
            "pokemon_stats": [self.pokemon_stat.id],  # Assuming a field for PokemonStats
            "species": self.species.id,  # Species ID
            "types": [self.type.id],  # Type IDs
            "held_items": [self.item.id],  # Item IDs
            "abilities": [self.ability.id],  # Ability IDs
            "moves": [self.move.id],  # Move IDs
        }
        
        response = self.client.post(url, data)
        
        # Check if the response redirects to the success_url (index page in this case)
        self.assertRedirects(response, reverse("index"))  # Ensure redirection happens
        
        # Check if the Pokémon was actually created in the database
        self.assertEqual(Pokemon.objects.count(), 1)
        self.assertEqual(Pokemon.objects.first().name, "Pikachu")
        self.assertEqual(Pokemon.objects.first().sprite, "pikachu_sprite_url")
        self.assertEqual(Pokemon.objects.first().base_experience, 112)
        self.assertEqual(Pokemon.objects.first().height, 4)
        self.assertEqual(Pokemon.objects.first().weight, 60)
        self.assertEqual(Pokemon.objects.first().species.name, "Electric Mouse")
        self.assertEqual(Pokemon.objects.first().types.first().name, "Electric")
        self.assertEqual(Pokemon.objects.first().held_items.first().name, "Thunder Stone")
        self.assertEqual(Pokemon.objects.first().abilities.first().name, "Static")
        self.assertEqual(Pokemon.objects.first().moves.first().name, "Thunderbolt")


class ViewAccessTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a user for login
        cls.user = User.objects.create_user(username="testuser", password="testpassword")
        
        # Create related objects (Stat, PokemonStat, Species, Type, Item, Ability, Move)
        cls.stat = Stat.objects.create(name="Speed")
        cls.pokemon_stat = PokemonStat.objects.create(base_stat=60, effort=2, stat=cls.stat)
        
        cls.species = Species.objects.create(name="Electric Mouse")
        cls.type = Type.objects.create(name="Electric")
        cls.item = Item.objects.create(name="Thunder Stone")
        cls.ability = Ability.objects.create(name="Static")
        cls.move = Move.objects.create(name="Thunderbolt")
        
        # Create a Pokémon object for tests that need it
        cls.pokemon = Pokemon.objects.create(
            name="Pikachu",
            sprite="pikachu_sprite_url",
            base_experience=112,
            height=4,
            weight=60,
            species=cls.species
        )
        cls.pokemon.pokemon_stats.add(cls.pokemon_stat)
        cls.pokemon.types.add(cls.type)
        cls.pokemon.held_items.add(cls.item)
        cls.pokemon.abilities.add(cls.ability)
        cls.pokemon.moves.add(cls.move)

    def test_create_pokemon_view_access_when_logged_in(self):
        """
        Test if logged-in users can access the CreatePokemonView.
        """
        self.client.login(username="testuser", password="testpassword")
        url = reverse("create_pokemon")  # Adjust this URL name based on your urls.py
        response = self.client.get(url)
        
        # Check if the response status is 200 OK (valid response)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "create_pokemon.html")

    def test_create_pokemon_view_access_when_logged_out(self):
        """
        Test if logged-out users are redirected to the login page when trying to access CreatePokemonView.
        """
        url = reverse("create_pokemon")  # Adjust this URL name based on your urls.py
        response = self.client.get(url)
        
        # Check if the response redirects to the login page
        self.assertRedirects(response, f"/login/?next={url}")
    
    def test_update_pokemon_view_access_when_logged_in(self):
        """
        Test if logged-in users can access the UpdatePokemonView.
        """
        self.client.login(username="testuser", password="testpassword")
        url = reverse("update_pokemon", kwargs={"pk": self.pokemon.id})  # Adjust URL based on your URL pattern
        response = self.client.get(url)
        
        # Check if the response status is 200 OK (valid response)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "update_pokemon.html")

    def test_update_pokemon_view_access_when_logged_out(self):
        """
        Test if logged-out users are redirected to the login page when trying to access UpdatePokemonView.
        """
        url = reverse("update_pokemon", kwargs={"pk": self.pokemon.id})  # Adjust URL based on your URL pattern
        response = self.client.get(url)
        
        # Check if the response redirects to the login page
        self.assertRedirects(response, f"/login/?next={url}")
    
    def test_delete_pokemon_view_access_when_logged_in(self):
        """
        Test if logged-in users can access the DeletePokemonView.
        """
        self.client.login(username="testuser", password="testpassword")
        url = reverse("delete_pokemon", kwargs={"pk": self.pokemon.id})  # Adjust URL based on your URL pattern
        response = self.client.get(url)
        
        # Check if the response status is 200 OK (valid response)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "delete_pokemon.html")

    def test_delete_pokemon_view_access_when_logged_out(self):
        """
        Test if logged-out users are redirected to the login page when trying to access DeletePokemonView.
        """
        url = reverse("delete_pokemon", kwargs={"pk": self.pokemon.id})  # Adjust URL based on your URL pattern
        response = self.client.get(url)
        
        # Check if the response redirects to the login page
        self.assertRedirects(response, f"/login/?next={url}")
    
