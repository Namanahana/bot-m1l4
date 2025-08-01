import aiohttp  # A library for asynchronous HTTP requests
import random

class Pokemon:
    pokemons = {}

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.abilities = None
        self.base_experience = None
        self.level = 1
        self.hunger = 100  # Full at start
        self.exp = 0
        self.rare = False
                # Inside __init__
        self.rare = random.random() < 0.05  # 5% chance to get rare Pokémon


        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer]

    def feed(self, food_amount=20):
        self.hunger = min(100, self.hunger + food_amount)
        self.exp += food_amount // 2
        return f"{self.name} has been fed. Hunger: {self.hunger}/100. EXP: {self.exp}"

    def level_up(self):
        level_ups = self.exp // 100
        if level_ups > 0:
            self.level += level_ups
            self.exp %= 100
            return f"{self.name} leveled up! Now at Level {self.level}!"
        return f"{self.name} needs more EXP to level up."
    
    def get_achievements(self):
        achievements = []
        if self.level >= 5:
            achievements.append("Level 5 Trainer 🎯")
        if self.hunger >= 90:
            achievements.append("Well-fed Pokémon 🍗")
        if self.rare:
            achievements.append("Rare Pokémon Collector 🌟")

        return "Achievements: " + ", ".join(achievements) if achievements else "No achievements yet."


    async def get_name(self):
        # An asynchronous method to get the name of a pokémon via PokeAPI
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # URL API for the request
        async with aiohttp.ClientSession() as session:  # Opening an HTTP session
            async with session.get(url) as response:  # Sending a GET request
                if response.status == 200:
                    data = await response.json()  # Receiving and decoding JSON response
                    return data['forms'][0]['name']  # Returning a Pokémon's name
                else:
                    return "Pikachu"  # Return the default name if the request fails

    async def info(self):
        # A method that returns information about the pokémon
        if not self.name:
            self.name = await self.get_name()  # Retrieving a name if it has not yet been uploaded
            self.base_experience = await self.get_base_experience()
            self.abilities = await self.get_abilities()
            rarity = "🌟RARE🌟" if self.rare else "Common"
            self.types = await self.get_types()
        return f"The name of your Pokémon: {self.name} ({rarity})\nLevel: {self.level}\nBase Experience: {self.base_experience}\nAbilities: {self.abilities}\nTypes: {self.types}"# Returning the string with the Pokémon's name

    async def show_img(self):
        # An asynchronous method to retrieve the URL of a pokémon image via PokeAPI
        # An asynchronous method to get the name of a pokémon via PokeAPI
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # URL API for the request
        async with aiohttp.ClientSession() as session:  # Opening an HTTP session
            async with session.get(url) as response:  # Sending a GET request
                if response.status == 200:
                    data = await response.json()  # Receiving and decoding JSON response
                    return data['sprites']['other']['showdown']['front_shiny']  # Returning a Pokémon's name
                else:
                    return "Image not found"  # Return the default name if the request fails

    async def get_base_experience(self):
        # An asynchronous method to get the name of a pokémon via PokeAPI
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # URL API for the request
        async with aiohttp.ClientSession() as session:  # Opening an HTTP session
            async with session.get(url) as response:  # Sending a GET request
                if response.status == 200:
                    data = await response.json()  # Receiving and decoding JSON response
                    return data['base_experience']  # Returning a Pokémon's name
                else:
                    return "Base experience not found"  # Return the default name if the request fails
                
    async def get_abilities(self):
        # An asynchronous method to get the name of a pokémon via PokeAPI
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # URL API for the request
        async with aiohttp.ClientSession() as session:  # Opening an HTTP session
            async with session.get(url) as response:  # Sending a GET request
                if response.status == 200:
                    data = await response.json()  # Receiving and decoding JSON response
                    return data['abilities'][0]['ability']['name']  # Returning a Pokémon's name
                else:
                    return "Abilities not found"  # Return the default name if the request fails
                
    async def get_types(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return ", ".join([t['type']['name'] for t in data['types']])
                return "Unknown"
