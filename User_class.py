from random import randint
import time

class User:

    def __init__(self, name, pokemon):
        self.name = name
        self.pokeballs = [20,0,0]
        self.pokemons = [pokemon]
        self.games_won = 0

    def get_name(self):
        return self.name

    def get_pokemon_list(self):
        return [poke.get_name() for poke in self.pokemons]

    def get_pokeballs(self):
        return self.pokeballs

    def get_games_won(self):
        return self.games_won

    def list_pokemons(self):
        print("\nYour pokemon: ")
        for i,pokemon in enumerate(self.pokemons):
            print(f"Pokemon {i+1}: {pokemon.get_name()}")
    
    def list_pokeballs(self):
        print("Pokeballs currently owned:")
        ball_types = ["pokeballs", "great balls", "master balls"]
        print("Type of ball\t# Owned")
        for i,ball in enumerate(self.pokeballs):
            print(ball_types[i],"\t",ball,sep='')

    def new_pokemon(self, pokemon):
        self.pokemons.append(pokemon)

    def new_pokeballs(self,start):
        if time.time() - start <= 180:
            print(f"You can't get any new pokeballs now. You need to wait another {round(180 - (time.time() - start),1)} seconds.")
            return start
        rng = randint(0,100)
        if rng < 80:
            num = randint(1,5)
            new = [num, "pokeball"]
        elif rng <= 98:
            num = randint(1,5)
            new = [num, "great ball"]
        else:
            num = randint(1,3)
            new = [num, "master ball"]
        print(f"Congratulations, you rolled {rng}! You won {new[0]} {new[1]}s.")

        if new[1] == "pokeball":
            self.pokeballs[0] += new[0]
        elif new[1] == "great ball":
            self.pokeballs[1] += new[0]
        else:
            self.pokeballs[2] += new[0]

        return time.time()

    def get_pokemon(self,poke_name):
        for poke in self.pokemons:
            if poke.get_name() == poke_name:
                return poke

    def best_pokemon_stats(self):
        best = [0,0,0]
        for poke in self.pokemons:
            if sum(poke.get_stats()) > sum(best):
                best = poke.get_stats()
        return best

    def use_pokeball(self,ball_type):
        self.pokeballs[ball_type] -= 1

    def won_game(self):
        self.games_won += 1
