from random import randint
import pokemon.master as pk

asciis = pk.catch_em_all()

class Pokemon:

     def __init__(self, name, typ, pokedex_entry, owner=False):
          self.name = name
          self.type = typ
          self.owner = owner
          self.CP = 0
          self.stats = [0, 0, 0] ## [attack, defense, stamina] - max 15
          self.IV = 0
          self.defending = False
          self.pokedex_entry = pokedex_entry

     def get_name(self):
          return self.name

     def get_type(self):
          return self.type

     def get_owner(self):
          return self.owner

     def get_stats(self):
          return self.stats

     def get_IV(self):
          return self.IV

     def get_CP(self):
          return self.CP

     def get_pokedex_entry(self):
          return self.pokedex_entry

     def get_ascii_art(self):
          return asciis[str(int(self.get_pokedex_entry()))]['ascii']

     def display_details(self):
          print("Name:\t\t",self.get_name())
          print("Pokedex Entry:\t",self.get_pokedex_entry())
          print("Type:\t\t",self.get_type())
          print("CP:\t\t",self.get_CP())
          stats = self.get_stats()
          print("Attack:\t\t",stats[0])
          print("Defense:\t",stats[1])
          print("Stamina:\t",stats[2])
          print("IV:\t\t",self.get_IV())
          print(self.get_ascii_art())
          
     def power_up(self, value):
          self.CP += value
          return self.CP

     def set_stats(self, attack, defense, stamina):
          test = [attack, defense, stamina]
          if max(test) > 15 or min(test) < 0:
               print("Sorry, values must be between 0 and 15.")
          else:
               self.stats = test
               self.IV = round(sum(self.stats)/45*100,2)
          return self.IV

     def catch(self, player):
          still_there = True
          ball_type = 0
          while still_there:
               ball_types = ["pokeball", "great ball", "master ball"]
               pokeball = str(input("Do you want to use a pokeball, great ball or master ball? "))
               while pokeball not in ball_types:
                    player.list_pokeballs()
                    pokeball = str(input("Please enter one of the following: pokeball, great ball or master ball? "))
               while player.get_pokeballs()[ball_types.index(pokeball)] <= 0:
                    print(f"You do not have any {pokeball}s! Please select a valid entry.")
                    pokeball = str(input("Please enter one of the following for which you have a nonzero quantity: pokeball, great ball or master ball? "))
                    while pokeball not in ball_types:
                         player.list_pokeballs()
                         pokeball = str(input("Please enter one of the following: pokeball, great ball or master ball? "))
               user = player.get_name()
               if pokeball == "pokeball":
                    ball_type = 0
                    nums = [randint(1,6), randint(1,6)]
                    if nums[0] == nums[1]:
                         self.owner = user
               elif pokeball == "great ball":
                    ball_type = 1
                    nums = [randint(1,4), randint(1,4)]
                    if nums[0] == nums[1]:
                         self.owner = user
               elif pokeball == "master ball":
                    ball_type = 2
                    nums = [randint(1,99), randint(1,99)]
                    if nums[0] != nums[1]:
                         self.owner = user
               player.use_pokeball(ball_type)
               if bool(self.owner):
                    return True
               num1 = randint(1,10)
               num2 = randint(1,10)
               if num1 == num2:
                    still_there = False
                    return "ran away"
               if still_there and (not bool(self.owner)):
                    try_again = str(input("You could not catch them in this attempt but they are still here. Would you like to try again? If no, enter \"X\" "))
                    if try_again == "X":
                         break
          return bool(self.owner)

     def fight_move(self,move):
          if move == "attack":
               return self.stats[0]*(1/2 + randint(1,5)/10)
          else:
               self.defending = True

     def receive_damage(self,dmg,game_stats,player):
          if self.get_name() not in player.get_pokemon_list():
               k = 1
          else:
               k = 0
          net_dmg = dmg - bool(self.defending)*self.stats[1]*(1+randint(1,5)/10)
          self.defending = False
          if net_dmg <= 0:
               net_dmg = 0
          game_stats[k][2] -= net_dmg
          if game_stats[k][2] <= 0:
               game_stats[k][2] = 0
          return [game_stats,net_dmg]
