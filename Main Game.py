import random
import time

username = print("Enter your hero's name: ")

potions = [
    {"name": "Health_Potion", "Gives_Health": random.randint(3, 5)},
    {"name": "Strength_Potion", "Gives_Strength": random.randint(5, 9)},
    {"name": "Sheild_Potion", "Gives_Sheild": random.randint(10, 25)},
]

loot = [
    {"name": "Loot_Potion", "Gives_Shards": random.randint(10, 25)},
    {"name": "Wood_Sword", "Damage": "3" }, # probability number = 3 (1 in 10)
    {"name": "Stone_Sword", "Damage": "7" }, # probability number = 8 (1 in 20)
    {"name": "Iron_Sword", "Damage": "11" }, # probability number = 17 (1 in 35)
    {"name": "Diamond_Sword", "Damage": "17" }, # probability number = 28 (1 in 50)
    {"name": "VoidCarver", "Damage": "25" },# probability number = 35 ( 1 in 250)
    {"name": "DawnSpire", "Damage": "50" }, # probability number = 55 (1 in 500)
]
sword_prompts = [
    {"VoidCarver_Prompt": "A pitch black sword that has been passed down from millions of generations of Demons"},
    {"DawnSpire_Prompt": "A Blade that glows with the first light of a new empire"}
]

player = {
    "Name" : username,
    "hp" : "30",
    "start_attack" : "0",
    "defense" : "7",
    "Speed" : "4",
    "Shards" : "10",
    "Sheild": "50",
    "Sword": "Wood_Sword",
    "Inventory" : ["Health Potion"]
}

basic_monsters = [
    {"name": "Zombie", "hp": 25, "Attack": 3,"Shards_Dropped": random.randint(1,25)},
    {"name": "Orc", "hp": 35, "Attack": 7, "Shards_Dropped": random.randint(10,50)},
    {"name": ""}
]

#print(player["start_attack"])

def equipped_weapon(new_weapon):
    player["Sword"] = new_weapon

    for item in loot:
        if item["name"] == new_weapon:
            player["Sword"] = item["Damage"]
            break


equipped_weapon("DawnSpire")
print(player["start_attack"])

