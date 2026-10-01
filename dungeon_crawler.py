"""
DUNGEON CRAWLER
A text-based RPG adventure game.

Explore rooms, fight monsters, collect loot, level up, and try to
defeat the Dragon King at the bottom of the dungeon.
"""

import random
import time
import sys


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

def slow_print(text, delay=0.015):
    """Print text with a small delay per character for dramatic effect."""
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def pause():
    input("\nPress Enter to continue...")


def divider():
    print("\n" + "-" * 50 + "\n")


def clamp(value, low, high):
    return max(low, min(value, high))


# ---------------------------------------------------------------------------
# Items
# ---------------------------------------------------------------------------

WEAPONS = {
    "Rusty Dagger": {"damage": 4, "price": 0},
    "Iron Sword": {"damage": 8, "price": 25},
    "Steel Axe": {"damage": 12, "price": 55},
    "Enchanted Blade": {"damage": 18, "price": 120},
    "Dragon Slayer": {"damage": 28, "price": 250},
}

ARMORS = {
    "Cloth Robe": {"defense": 1, "price": 0},
    "Leather Armor": {"defense": 4, "price": 20},
    "Chainmail": {"defense": 8, "price": 50},
    "Plate Armor": {"defense": 14, "price": 110},
    "Dragonscale Mail": {"defense": 22, "price": 240},
}

POTIONS = {
    "Small Potion": {"heal": 15, "price": 10},
    "Medium Potion": {"heal": 35, "price": 25},
    "Large Potion": {"heal": 70, "price": 50},
}


# ---------------------------------------------------------------------------
# Monsters
# ---------------------------------------------------------------------------

class Monster:
    def __init__(self, name, hp, attack, defense, gold_reward, xp_reward):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.gold_reward = gold_reward
        self.xp_reward = xp_reward

    def is_alive(self):
        return self.hp > 0


MONSTER_TABLE = [
    lambda floor: Monster("Giant Rat", 12 + floor * 2, 3 + floor, 0, 5 + floor, 8 + floor * 2),
    lambda floor: Monster("Goblin", 18 + floor * 3, 5 + floor, 1, 8 + floor, 12 + floor * 2),
    lambda floor: Monster("Skeleton", 25 + floor * 3, 7 + floor, 2, 12 + floor, 16 + floor * 2),
    lambda floor: Monster("Orc Brute", 35 + floor * 4, 10 + floor, 3, 18 + floor, 24 + floor * 3),
    lambda floor: Monster("Dark Mage", 28 + floor * 4, 13 + floor, 1, 22 + floor, 28 + floor * 3),
]

BOSS = lambda: Monster("The Dragon King", 220, 22, 8, 500, 300)


def spawn_monster(floor):
    generator = random.choice(MONSTER_TABLE)
    return generator(floor)


# ---------------------------------------------------------------------------
# Player
# ---------------------------------------------------------------------------

class Player:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.xp = 0
        self.xp_to_next = 30
        self.max_hp = 60
        self.hp = 60
        self.base_attack = 6
        self.base_defense = 2
        self.gold = 20
        self.weapon = "Rusty Dagger"
        self.armor = "Cloth Robe"
        self.inventory = {"Small Potion": 2}
        self.floor = 1

    # -- derived stats --
    @property
    def attack(self):
        return self.base_attack + WEAPONS[self.weapon]["damage"]

    @property
    def defense(self):
        return self.base_defense + ARMORS[self.armor]["defense"]

    def is_alive(self):
        return self.hp > 0

    def heal(self, amount):
        self.hp = clamp(self.hp + amount, 0, self.max_hp)

    def take_damage(self, amount):
        dmg = max(1, amount - self.defense)
        self.hp = clamp(self.hp - dmg, 0, self.max_hp)
        return dmg

    def gain_xp(self, amount):
        self.xp += amount
        print(f"You gained {amount} XP!")
        while self.xp >= self.xp_to_next:
            self.xp -= self.xp_to_next
            self.level_up()

    def level_up(self):
        self.level += 1
        self.max_hp += 15
        self.hp = self.max_hp
        self.base_attack += 3
        self.base_defense += 1
        self.xp_to_next = int(self.xp_to_next * 1.4)
        slow_print(f"\n*** You leveled up! You are now level {self.level}! ***")
        print(f"Max HP: {self.max_hp} | Attack: {self.attack} | Defense: {self.defense}")

    def status(self):
        print(f"\n{self.name} | Lv.{self.level} | Floor {self.floor}")
        print(f"HP: {self.hp}/{self.max_hp} | XP: {self.xp}/{self.xp_to_next} | Gold: {self.gold}")
        print(f"Weapon: {self.weapon} (+{WEAPONS[self.weapon]['damage']} dmg) | "
              f"Armor: {self.armor} (+{ARMORS[self.armor]['defense']} def)")

    def show_inventory(self):
        if not self.inventory:
            print("Your inventory is empty.")
            return
        print("Inventory:")
        for item, count in self.inventory.items():
            print(f"  {item} x{count}")

    def use_potion(self):
        potions_owned = [p for p in self.inventory if p in POTIONS and self.inventory[p] > 0]
        if not potions_owned:
            print("You have no potions!")
            return False
        print("Choose a potion to use:")
        for i, p in enumerate(potions_owned, 1):
            print(f"  {i}. {p} (heals {POTIONS[p]['heal']} HP) x{self.inventory[p]}")
        choice = input("> ").strip()
        if not choice.isdigit() or not (1 <= int(choice) <= len(potions_owned)):
            print("Invalid choice.")
            return False
        potion = potions_owned[int(choice) - 1]
        self.heal(POTIONS[potion]["heal"])
        self.inventory[potion] -= 1
        if self.inventory[potion] == 0:
            del self.inventory[potion]
        print(f"You drink the {potion} and heal to {self.hp}/{self.max_hp} HP.")
        return True


# ---------------------------------------------------------------------------
# Combat
# ---------------------------------------------------------------------------

def combat(player, monster):
    divider()
    slow_print(f"A wild {monster.name} appears! (HP: {monster.hp})")

    while player.is_alive() and monster.is_alive():
        print(f"\nYour HP: {player.hp}/{player.max_hp}  |  {monster.name} HP: {monster.hp}/{monster.max_hp}")
        print("1. Attack  2. Use Potion  3. Flee")
        choice = input("> ").strip()

        if choice == "1":
            dmg = max(1, player.attack - monster.defense + random.randint(-2, 3))
            monster.hp = clamp(monster.hp - dmg, 0, monster.max_hp)
            print(f"You strike the {monster.name} for {dmg} damage!")
        elif choice == "2":
            player.use_potion()
        elif choice == "3":
            if random.random() < 0.5:
                print("You successfully flee the battle!")
                return "fled"
            else:
                print("You failed to escape!")
        else:
            print("Invalid choice. You hesitate and lose your turn!")

        if monster.is_alive():
            dmg_taken = player.take_damage(monster.attack + random.randint(-2, 2))
            print(f"The {monster.name} hits you for {dmg_taken} damage!")
        else:
            break

        if not player.is_alive():
            break

    if not player.is_alive():
        return "dead"

    if not monster.is_alive():
        slow_print(f"\nYou defeated the {monster.name}!")
        gold = monster.gold_reward + random.randint(0, 5)
        player.gold += gold
        print(f"You loot {gold} gold.")
        player.gain_xp(monster.xp_reward)
        return "won"

    return "unknown"


# ---------------------------------------------------------------------------
# Shop
# ---------------------------------------------------------------------------

def shop(player):
    while True:
        divider()
        print(f"=== SHOP ===  (Gold: {player.gold})")
        print("1. Buy Weapon")
        print("2. Buy Armor")
        print("3. Buy Potion")
        print("4. Sell nothing / Leave shop")
        choice = input("> ").strip()

        if choice == "1":
            buy_from_table(player, WEAPONS, "weapon")
        elif choice == "2":
            buy_from_table(player, ARMORS, "armor")
        elif choice == "3":
            buy_potion(player)
        elif choice == "4":
            print("You leave the shop.")
            break
        else:
            print("Invalid choice.")


def buy_from_table(player, table, kind):
    print(f"\nAvailable {kind}s:")
    items = list(table.items())
    for i, (name, stats) in enumerate(items, 1):
        key = "damage" if kind == "weapon" else "defense"
        print(f"  {i}. {name} (+{stats[key]} {key}) - {stats['price']} gold")
    choice = input("Buy which item? (0 to cancel) > ").strip()
    if not choice.isdigit() or int(choice) == 0:
        return
    idx = int(choice) - 1
    if not (0 <= idx < len(items)):
        print("Invalid choice.")
        return
    name, stats = items[idx]
    if player.gold < stats["price"]:
        print("You can't afford that.")
        return
    player.gold -= stats["price"]
    if kind == "weapon":
        player.weapon = name
    else:
        player.armor = name
    print(f"You equip the {name}!")


def buy_potion(player):
    print("\nAvailable potions:")
    items = list(POTIONS.items())
    for i, (name, stats) in enumerate(items, 1):
        print(f"  {i}. {name} (heals {stats['heal']}) - {stats['price']} gold")
    choice = input("Buy which potion? (0 to cancel) > ").strip()
    if not choice.isdigit() or int(choice) == 0:
        return
    idx = int(choice) - 1
    if not (0 <= idx < len(items)):
        print("Invalid choice.")
        return
    name, stats = items[idx]
    if player.gold < stats["price"]:
        print("You can't afford that.")
        return
    player.gold -= stats["price"]
    player.inventory[name] = player.inventory.get(name, 0) + 1
    print(f"You bought a {name}!")


# ---------------------------------------------------------------------------
# Dungeon exploration
# ---------------------------------------------------------------------------

def explore_floor(player):
    divider()
    slow_print(f"You descend to floor {player.floor} of the dungeon...")
    event = random.choices(
        ["monster", "treasure", "shop", "trap", "nothing"],
        weights=[45, 20, 10, 15, 10],
        k=1
    )[0]

    if event == "monster":
        monster = spawn_monster(player.floor)
        result = combat(player, monster)
        if result == "dead":
            return "dead"
    elif event == "treasure":
        gold = random.randint(10, 20) * player.floor
        print(f"You find a treasure chest containing {gold} gold!")
        player.gold += gold
        if random.random() < 0.3:
            potion = random.choice(list(POTIONS.keys()))
            player.inventory[potion] = player.inventory.get(potion, 0) + 1
            print(f"There's also a {potion} inside!")
    elif event == "shop":
        print("You stumble upon a traveling merchant!")
        shop(player)
    elif event == "trap":
        dmg = random.randint(5, 15)
        player.hp = clamp(player.hp - dmg, 0, player.max_hp)
        print(f"You triggered a trap! You take {dmg} damage.")
        if not player.is_alive():
            return "dead"
    else:
        print("This floor is quiet. You rest for a moment and recover a bit.")
        player.heal(10)

    player.floor += 1
    return "continue"


def boss_fight(player):
    divider()
    slow_print("The air grows cold. You've reached the heart of the dungeon.")
    slow_print("The DRAGON KING awakens...")
    boss = BOSS()
    result = combat(player, boss)
    return result


# ---------------------------------------------------------------------------
# Main game loop
# ---------------------------------------------------------------------------

def main_menu(player):
    while True:
        divider()
        print("=== DUNGEON CRAWLER ===")
        print("1. Descend further into the dungeon")
        print("2. Check status")
        print("3. Check inventory")
        print("4. Use a potion")
        print("5. Quit game")
        choice = input("> ").strip()

        if choice == "1":
            if player.floor >= 10:
                result = boss_fight(player)
                if result == "won":
                    slow_print("\n*** YOU HAVE DEFEATED THE DRAGON KING! ***")
                    slow_print("You are victorious! The dungeon crumbles behind you.")
                    return
                elif result == "dead":
                    game_over(player)
                    return
                elif result == "fled":
                    print("You retreat from the boss room to gather your strength.")
            else:
                result = explore_floor(player)
                if result == "dead":
                    game_over(player)
                    return
        elif choice == "2":
            player.status()
        elif choice == "3":
            player.show_inventory()
        elif choice == "4":
            player.use_potion()
        elif choice == "5":
            print("Thanks for playing!")
            return
        else:
            print("Invalid choice.")


def game_over(player):
    divider()
    slow_print(f"You have fallen on floor {player.floor} of the dungeon...")
    slow_print(f"Final Level: {player.level}  |  Gold collected: {player.gold}")
    slow_print("GAME OVER")


def intro():
    slow_print("=" * 50)
    slow_print("           WELCOME TO DUNGEON CRAWLER")
    slow_print("=" * 50)
    slow_print("\nLegends speak of a dungeon with ten floors, guarded")
    slow_print("by monsters, traps, and treasure. At its heart sleeps")
    slow_print("the Dragon King. Only the bravest adventurers return.\n")
    name = input("Enter your hero's name: ").strip() or "Adventurer"
    return Player(name)


if __name__ == "__main__":
    hero = intro()
    slow_print(f"\nGood luck, {hero.name}. The dungeon awaits...")
    pause()
    main_menu(hero)
