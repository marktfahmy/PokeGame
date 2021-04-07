from Pokemon_class import Pokemon
from User_class import User
from random import randint
import pokemon.master as pk
import pandas as pd
import numpy as np
import time

pokemon_list = pd.DataFrame(pk.catch_em_all()).transpose()
pokemons = pokemon_list[['id','name','type']]
pokemons.loc[:,'type'] = pokemons.loc[:,'type'].apply(lambda x: x[0])
## this gives a stupid warning that doesn't make any sense
starters = pokemons.iloc[[0,3,6]].values

print("Welcome to the best (not really) Pokemon game you'll ever play!")
name = str(input("What is your name? "))

print(f"Hey, {name}. To get started, you'll need to choose a starter Pokemon. Your options are:")
for i,option in enumerate(starters):
    print(i+1,". ",option[1],sep="")
poke = str(input("Which one would you like? "))
while poke not in starters:
    print("You must choose one of the following starter pokemon: Bulbasaur, Charmander, Squirtle")
    poke = str(input("What is your starter pokemon? "))
poke_info = pokemons.iloc[np.where(pokemons.values[:,1]==poke)[0][0],:]
starter = Pokemon(poke,poke_info[2],poke_info[0],name)
player = User(name, starter)
starter.set_stats(2, 1, 3)
start = time.time()


def get_input(type_of_data,options):
    user_input = str(input()).strip()

    if type_of_data == "dict":
        if user_input.lower() not in options.keys() and user_input.upper() not in options.keys():
            print("Please enter one of the following options:")
            for key in options.keys():
                print(key,end='\t\t')
            print()
            user_input = str(input())

        while user_input.lower() not in options.keys() and user_input.upper() not in options.keys():
            print("Please enter one of the following options:")
            for key in options.keys():
                print(key,options[key],sep='\t')
            user_input = str(input())
    else:
        if user_input not in options:
            print("Please enter one of the following options:")
            for entry in options:
                print(entry,end='\t\t')
            print()
            user_input = str(input())

        while user_input not in options:
            print("Please enter one of the following options:")
            for i,entry in enumerate(options):
                print(i+1,entry,sep='\t')
            user_input = str(input())
    return user_input

def check_outcome(game_stats):
    if game_stats[0][2] == 0:
        print(f"You lost the match. Your pokemon has 0 stamina remaining.\n")
        return "computer"
    elif game_stats[1][2] == 0:
        print(f"Congratulations! You won the match. You can now upgrade your pokemon.\n")
        return "user"
    return False

def upgrade_pokemon(pokemon):
    options = {"attack": "This determines how much damage your {pokemon.get_name()} deals in battle.", "defense": "This determines how much damage is deflected from an attack received while defending.", "stamina": "This determines whether your pokemon is able to continue fighting or if they lose."}
    print(f"You can upgrade one of your {pokemon.get_name()}'s stats now. Would you like to upgrade attack, defense or stamina?")
    choice = get_input("dict",options)
    conv_to_indices = {"attack": 0, "defense": 1, "stamina": 2}
    index = conv_to_indices[choice]
    if pokemon.get_stats()[index] == 15:
        print("This stat is already maxxed out! Please make another selection")
        upgrade_pokemon(pokemon)

    new_stats = pokemon.get_stats()
    boost = round(1/2+1/2*(sum(new_stats)/6*float(np.random.rand(1))),2)
    new_stats[index] += boost
    pokemon.set_stats(new_stats[0], new_stats[1], new_stats[2])
    print(f"Congratulations, your {pokemon.get_name()}'s {choice} has been increased by {boost}!")

def auto_move(user_poke, opponent, game_stats):
    choice = randint(1,10)
    if choice <= 7:
        dmg = opponent.fight_move("attack")
        [game_stats,net_dmg] = user_poke.receive_damage(dmg,game_stats,player)
        print(f"{round(net_dmg,2)} damage dealt to {user_poke.get_name()}. They now have {round(game_stats[0][2],2)} stamina remaining.")
    elif choice <= 9:
        print(f"{opponent.get_name()} is now defending.")
        opponent.fight_move("defend")
    else:
        return "ran"

def player_move(user_poke, opponent, game_stats):
    print("\nWould you like to attack, defend, run away or try and catch the opposing pokemon?")
    move_options = {"attack": "Use an attacking move on the other pokemon.", "defend": "Activate your pokemon's defense.", "run": "Run away from this pokemon and end this match.", "catch": "Try to catch the opponent pokemon.\n"}
    move = get_input("dict",move_options).lower()
    if move == "attack":
        dmg = user_poke.fight_move(move)
        [game_stats,net_dmg] = opponent.receive_damage(dmg,game_stats,player)
        print(f"{round(net_dmg,2)} damage dealt to {opponent.get_name()}. They now have {round(game_stats[1][2],2)} stamina remaining.")
    elif move == "catch":
        if game_stats[1][2] <= 0.5*opponent.get_stats()[2]:
            attempt = opponent.catch(player)
            if attempt:
                player.new_pokemon(opponent)
                return "caught"
            elif attempt == "ran away":
                return "opp_ran"
        else:
            print("They have too much stamina remaining for you to try and catch them. Try again in a few moves.")
            player_move(user_poke, opponent, game_stats)
    elif move == "defend":
        print(f"{user_poke.get_name()} is now defending.")
        user_poke.fight_move("defend")
    else:
        return "ran"

print("\nAlright, let's get started. Here's your first opponent:")

playing = True
while playing:    
    k = randint(1,len(pokemons.iloc[0:-1,1]))-1
    opponent = Pokemon(pokemons.iloc[:,1][k],pokemons.iloc[:,2][k],pokemons.iloc[:,0][k])
    print(f"Your opponent is {opponent.get_name()}")

    adj_fac = 0.8 + 0.4*np.random.rand(2)
    new_stats = [min([15,round(player.best_pokemon_stats()[i]*adj_fac[i],2)]) for i in range(2)]
    opponent.set_stats(new_stats[0], new_stats[1], min([15,round(float(np.random.rand(1))+sum(player.best_pokemon_stats()) - sum(new_stats),2)]))
    opponent.display_details()
    
    poke = str(input("\nWhich of your pokemon do you want to use? ")).strip()
    while poke not in player.get_pokemon_list():
        print("You must choose one of your pokemon.")
        player.list_pokemons()
        poke = str(input("Which pokemon do you want to use? ")).strip()
    poke = player.get_pokemon(poke)
    
    game_stats = [poke.get_stats().copy(), opponent.get_stats().copy()]

    game_over = False
    while not game_over:
        player_outcome = player_move(poke, opponent, game_stats)

        if player_outcome == "ran":
            print("You ran away.")
            break
        elif player_outcome == "caught":
            print("Congratulations! You caught a new Pokemon: ",opponent.get_name())
            break
        elif player_outcome == "opp_ran":
            print(f"{opponent.get_name()} ran away after you tried catching them.")
            break

        game_over = check_outcome(game_stats)
        if game_over:
            if game_over == "user":
                player.won_game()
                poke.power_up(player.get_games_won())
                upgrade_pokemon(poke)
            break

        opponent_outcome = auto_move(poke, opponent, game_stats)

        if opponent_outcome == "ran":
            print("The opponent ran away.")
            break

        game_over = check_outcome(game_stats)

    options = {"EXIT": "\texit the game", "VIEW ONE": "look at a specific pokemon", "VIEW ALL": "list all your pokemon", "POKESTOP": "get pokeballs from a pokestop (can be done once per 5 minutes", "VIEW BALLS": "view how many of each pokeball you own", "PLAY AGAIN": "play another match\n"}
    print("Please enter which of the following you'd like to do:")
    for option in options:
        print(option,options[option],sep='\t')
    user_input = get_input("dict",options).upper()

    while user_input != "EXIT" and user_input != "PLAY AGAIN":
        if user_input == "VIEW ONE":
            print("Which pokemon would you like to look at?")
            choice = get_input("list",player.get_pokemon_list())
            viewing = player.get_pokemon(choice)
            viewing.display_details()
        elif user_input == "VIEW ALL":
            player.list_pokemons()
        elif user_input == "VIEW BALLS":
            player.list_pokeballs()
        elif user_input == "POKESTOP":
            start = player.new_pokeballs(start)

        print("What would you like to do now?")
        user_input = get_input("dict",options).upper()

    if user_input == "EXIT":
        print(f"Thanks for playing, {player.get_name()}!")
        playing = False
