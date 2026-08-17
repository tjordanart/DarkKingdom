import time
import random

# Colors
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"


# Type text one character at a time
def type_text(text, speed=0.02):
    for letter in text:
        print(letter, end="", flush=True)
        time.sleep(speed)
    print()


# Pause between scenes
def pause(seconds: float = 0.5):
    time.sleep(seconds)


# Battle function
# `stats` is a dict holding all the player's mutable state (health, gold,
# xp, level, potions, max_health, attack, character, special_attack).
# Because it's a mutable dict passed in, we can update it in place without
# ever needing "global" - which is what was causing the shadowing warnings.
def battle_enemy(stats, enemy_name, enemy_health, enemy_attack):

    # Special attack cooldown starts at zero
    special_cooldown = 0

    # Announce the enemy
    print("\n" + RED + "A " + enemy_name.upper() + " APPEARS!" + RESET + "\n")

    print(enemy_name + " Health: " + RED + str(enemy_health) + RESET)

    # Start the battle
    while stats["health"] > 0 and enemy_health > 0:

        # Show current battle stats
        print("\nYour Health: " + GREEN + str(stats["health"]) + RESET)
        print(enemy_name + " Health: " + RED + str(enemy_health) + RESET)
        print(CYAN + "------------------------------" + RESET)

        # Show special attack status
        if special_cooldown == 0:
            print("Special Attack: " + CYAN + "READY" + RESET)
        else:
            print(
                "Special Attack: "
                + YELLOW
                + str(special_cooldown)
                + " turns"
                + RESET
            )

        # Show battle choices
        print("\n1. Attack")
        print("2. Special Attack")
        print("3. Use Potion")
        print("4. Run")

        battle_choice = input(YELLOW + "\nWhat do you do? " + RESET)

        # Player attacks the enemy
        if battle_choice == "1":

            damage = random.randint(stats["attack"] - 5, stats["attack"] + 5)

            # 15% chance of critical hit
            critical_hit = random.randint(1, 100) <= 15

            if critical_hit:
                damage *= 2

                type_text("\nYou attack the " + enemy_name + "!")
                print(RED + "CRITICAL HIT!" + RESET)
                type_text("You deal " + str(damage) + " damage.")

            else:
                type_text("\nYou attack the " + enemy_name + "!")
                type_text("You deal " + str(damage) + " damage.")

            enemy_health -= damage

            # Enemy attacks if still alive
            if enemy_health > 0:
                enemy_damage = random.randint(5, enemy_attack)
                stats["health"] -= enemy_damage

                type_text("\nThe " + enemy_name + " attacks!")
                type_text("You take " + str(enemy_damage) + " damage.")

                # Werewolf healing ability
                if enemy_name == "Werewolf" and random.randint(1, 100) <= 25:

                    heal_amount = 20
                    enemy_health += heal_amount

                    type_text(
                        RED
                        + "The Werewolf howls and restores "
                        + str(heal_amount)
                        + " health!"
                        + RESET
                    )

        # Player uses special attack
        elif battle_choice == "2":

            if special_cooldown == 0:

                if stats["character"] == "Warrior":
                    damage = random.randint(25, 40)

                elif stats["character"] == "Wizard":
                    damage = random.randint(30, 45)

                else:
                    damage = random.randint(20, 50)

                enemy_health -= damage

                # Start cooldown
                special_cooldown = 3

                type_text("\nYou use " + stats["special_attack"] + "!")
                type_text("You deal " + str(damage) + " damage.")

                # Enemy attacks if still alive
                if enemy_health > 0:
                    enemy_damage = random.randint(5, enemy_attack)
                    stats["health"] -= enemy_damage

                    type_text("\nThe " + enemy_name + " attacks!")
                    type_text("You take " + str(enemy_damage) + " damage.")

            else:
                type_text("\nYour special attack is on cooldown.")

        # Player uses potion
        elif battle_choice == "3":

            if stats["potions"] > 0:

                heal = 30
                old_health = stats["health"]

                stats["health"] += heal

                if stats["health"] > stats["max_health"]:
                    stats["health"] = stats["max_health"]

                actual_heal = stats["health"] - old_health
                stats["potions"] -= 1

                type_text("\nYou drink a health potion.")
                type_text(
                    "You recover "
                    + str(actual_heal)
                    + " health."
                )

                type_text(
                    "Potions remaining: "
                    + str(stats["potions"])
                )

            else:
                type_text("\nYou don't have any potions.")

        # Player runs
        elif battle_choice == "4":

            type_text(
                "\nYou run away from the "
                + enemy_name
                + "."
            )

            return False

        # Invalid choice
        else:
            type_text("\nThat is not a valid choice.")

        # Reduce cooldown
        if special_cooldown > 0:
            special_cooldown -= 1

    # Enemy defeated
    if enemy_health <= 0:

        print(
            "\n"
            + GREEN
            + "The "
            + enemy_name
            + " has been defeated!"
            + RESET
        )

        # Give rewards
        stats["xp"] += 50
        stats["gold"] += 20

        type_text("You gained 50 XP.")
        type_text("You found 20 gold.")

        pause()

        # Check for level up
        if stats["xp"] >= stats["xp_needed"]:

            stats["level"] += 1
            stats["xp"] -= stats["xp_needed"]

            stats["max_health"] += 20
            stats["health"] = stats["max_health"]
            stats["attack"] += 5

            # Level-up information
            type_text(YELLOW + "\nLEVEL UP!" + RESET)

            type_text(
                YELLOW
                + "You are now Level "
                + str(stats["level"])
                + "!"
                + RESET
            )

            type_text(
                YELLOW
                + "Health increased to "
                + str(stats["max_health"])
                + "!"
                + RESET
            )

            type_text(
                YELLOW
                + "Attack increased to "
                + str(stats["attack"])
                + "!"
                + RESET
            )

            type_text(
                YELLOW
                + "You are fully healed!"
                + RESET
            )

        print("\nXP: " + str(stats["xp"]))
        print("Gold: " + YELLOW + str(stats["gold"]) + RESET)

        pause()

        return True

    # Player defeated
    elif stats["health"] <= 0:

        print(
            "\n"
            + RED
            + "You have been defeated."
            + RESET
        )

        type_text("Your adventure ends here.")

        return False

    return False


def run_castle_room_battle(stats, room_name):
    """Shared logic for the Armory/Dungeon rooms - picks a random enemy
    pair and runs the fight, returning whether the player won."""

    if room_name == "Armory":
        type_text("\nYou enter the armory.")
        type_text("Rusty weapons line the walls.")
        enemy = random.choice(["Skeleton", "Dark Soldier"])
        enemy_health = random.choice([70, 90])
        enemy_attack = random.choice([14, 17])
        reward = 40

    else:
        type_text("\nYou descend into the dungeon.")
        type_text("Something moves in the darkness.")
        enemy = random.choice(["Vampire", "Dark Mage"])
        enemy_health = random.choice([85, 75])
        enemy_attack = random.choice([18, 20])
        reward = 60

    defeated = battle_enemy(stats, enemy, enemy_health, enemy_attack)

    if defeated:
        type_text(
            "\nYou find a chest containing "
            + str(reward)
            + " gold!"
        )
        stats["gold"] += reward

    return defeated


def run_castle_merchant(stats):
    """Runs the merchant shop loop in the castle hallway."""

    pause()

    type_text("\nYou leave the chamber and enter a dark hallway.")

    pause()

    type_text("A mysterious merchant waits in the shadows.")

    pause()

    print("\n" + CYAN + "CASTLE MERCHANT" + RESET)

    type_text("\nYou may purchase weapons, potions, and upgrades.")

    # Track purchases
    weapon_purchased = False
    potions_bought = 0
    health_upgrade_purchased = False
    attack_upgrade_purchased = False

    # Merchant shop loop
    while True:

        print("\n" + YELLOW + "Gold: " + str(stats["gold"]) + RESET)

        print("\n1. Buy Weapon")
        print("2. Buy Potion (Max 3) - 20 gold")
        print("3. Health Upgrade - 30 gold (+20 Max Health)")
        print("4. Attack Upgrade - 30 gold (+5 Attack)")
        print("5. Leave Shop")

        shop_choice = input(
            YELLOW + "\nWhat would you like to buy? " + RESET
        ).strip()

        # Buy weapon
        if shop_choice == "1":

            if weapon_purchased:
                type_text("\nYou have already purchased a weapon.")

            else:
                print("\nChoose your weapon:")

                if stats["character"] == "Warrior":
                    print("1. Ironblade - 20 gold (+5 Attack)")
                    print("2. Great Sword - 40 gold (+10 Attack)")

                elif stats["character"] == "Rogue":
                    print("1. Shadow Dagger - 20 gold (+5 Attack)")
                    print("2. Ironfang - 40 gold (+10 Attack)")

                else:
                    print("1. Arcane Staff - 20 gold (+5 Attack)")
                    print("2. Enchanted Staff - 40 gold (+10 Attack)")

                weapon_choice = input(
                    YELLOW + "\nWhich weapon do you want? " + RESET
                ).strip()

                # Smaller weapon
                if weapon_choice == "1":

                    if stats["gold"] >= 20:

                        stats["gold"] -= 20
                        stats["attack"] += 5
                        weapon_purchased = True

                        if stats["character"] == "Warrior":
                            weapon_name = "Ironblade"
                        elif stats["character"] == "Rogue":
                            weapon_name = "Shadow Dagger"
                        else:
                            weapon_name = "Arcane Staff"

                        type_text("\nYou purchased the " + weapon_name + "!")
                        type_text("Attack increased by 5!")
                        print("Attack: " + str(stats["attack"]))

                    else:
                        type_text("\nYou don't have enough gold.")

                # Powerful weapon
                elif weapon_choice == "2":

                    if stats["gold"] >= 40:

                        stats["gold"] -= 40
                        stats["attack"] += 10
                        weapon_purchased = True

                        if stats["character"] == "Warrior":
                            weapon_name = "Great Sword"
                        elif stats["character"] == "Rogue":
                            weapon_name = "Ironfang"
                        else:
                            weapon_name = "Enchanted Staff"

                        type_text("\nYou purchased the " + weapon_name + "!")
                        type_text("Attack increased by 10!")
                        print("Attack: " + str(stats["attack"]))

                    else:
                        type_text("\nYou don't have enough gold.")

                else:
                    type_text("\nThat is not a valid choice.")

        # Buy potion
        elif shop_choice == "2":

            if potions_bought >= 3:
                type_text("\nYou have reached the maximum of 3 potions.")

            elif stats["gold"] >= 20:

                stats["gold"] -= 20
                stats["potions"] += 1
                potions_bought += 1

                type_text("\nYou purchased a health potion!")
                print("Potions: " + str(stats["potions"]))

            else:
                type_text("\nYou don't have enough gold.")

        # Health upgrade
        elif shop_choice == "3":

            if health_upgrade_purchased:
                type_text("\nYou have already purchased the Health Upgrade.")

            elif stats["gold"] >= 30:

                stats["gold"] -= 30
                stats["max_health"] += 20
                stats["health"] = stats["max_health"]
                health_upgrade_purchased = True

                type_text("\nYou purchased the Health Upgrade!")
                type_text("Maximum Health increased by 20!")
                type_text("You are fully healed!")
                print("Max Health: " + str(stats["max_health"]))

            else:
                type_text("\nYou don't have enough gold.")

        # Attack upgrade
        elif shop_choice == "4":

            if attack_upgrade_purchased:
                type_text("\nYou have already purchased the Attack Upgrade.")

            elif stats["gold"] >= 30:

                stats["gold"] -= 30
                stats["attack"] += 5
                attack_upgrade_purchased = True

                type_text("\nYou purchased the Attack Upgrade!")
                type_text("Attack increased by 5!")
                print("Attack: " + str(stats["attack"]))

            else:
                type_text("\nYou don't have enough gold.")

        # Leave shop
        elif shop_choice == "5":

            type_text("\nYou leave the merchant behind.")

            print("\nGold: " + YELLOW + str(stats["gold"]) + RESET)
            print("Attack: " + str(stats["attack"]))
            print("Max Health: " + str(stats["max_health"]))
            print("Potions: " + str(stats["potions"]))

            pause()

            break

        # Invalid shop choice
        else:
            type_text("\nThat is not a valid choice.")


def run_dark_king_battle(stats):
    """Runs the final boss fight against the Dark King."""

    dark_king_health = 180
    dark_king_max_health = 180
    dark_king_attack = 25
    dark_king_cooldown = 0

    while stats["health"] > 0 and dark_king_health > 0:

        print("\nYour Health: " + GREEN + str(stats["health"]) + RESET)
        print("Dark King Health: " + RED + str(dark_king_health) + RESET)
        print(CYAN + "------------------------------" + RESET)

        print("\n1. Attack")
        print("2. Special Attack")
        print("3. Use Potion")

        boss_choice = input(YELLOW + "\nWhat do you do? " + RESET).strip()

        # Player attacks Dark King
        if boss_choice == "1":

            damage = random.randint(stats["attack"] - 5, stats["attack"] + 5)
            critical_hit = random.randint(1, 100) <= 15

            if critical_hit:
                damage *= 2

                type_text("\nYou attack the Dark King!")
                print(RED + "CRITICAL HIT!" + RESET)
                type_text("You deal " + str(damage) + " damage.")

            else:
                type_text("\nYou attack the Dark King!")
                type_text("You deal " + str(damage) + " damage.")

            dark_king_health -= damage

        # Player uses special attack
        elif boss_choice == "2":

            if dark_king_cooldown == 0:

                if stats["character"] == "Warrior":
                    damage = random.randint(25, 40)
                elif stats["character"] == "Wizard":
                    damage = random.randint(30, 45)
                else:
                    damage = random.randint(20, 50)

                dark_king_health -= damage
                dark_king_cooldown = 3

                type_text("\nYou use " + stats["special_attack"] + "!")
                type_text("You deal " + str(damage) + " damage.")

            else:
                type_text("\nYour special attack is on cooldown.")

        # Player uses potion
        elif boss_choice == "3":

            if stats["potions"] > 0:

                heal = 30
                old_health = stats["health"]

                stats["health"] += heal

                if stats["health"] > stats["max_health"]:
                    stats["health"] = stats["max_health"]

                actual_heal = stats["health"] - old_health
                stats["potions"] -= 1

                type_text("\nYou drink a health potion.")
                type_text("You recover " + str(actual_heal) + " health.")
                type_text("Potions remaining: " + str(stats["potions"]))

            else:
                type_text("\nYou don't have any potions.")

        # Invalid choice
        else:
            type_text("\nThat is not a valid choice.")
            continue

        # Check if Dark King is defeated
        if dark_king_health <= 0:
            break

        # Dark King attacks
        dark_king_damage = random.randint(12, dark_king_attack)
        stats["health"] -= dark_king_damage

        type_text("\nThe Dark King attacks!")
        type_text("You take " + str(dark_king_damage) + " damage.")

        # Dark King healing ability
        if dark_king_health > 0 and random.randint(1, 100) <= 25:

            heal_amount = 20
            dark_king_health += heal_amount

            if dark_king_health > dark_king_max_health:
                dark_king_health = dark_king_max_health

            type_text(
                RED
                + "The Dark King raises his hand and restores 20 health!"
                + RESET
            )

        # Reduce special cooldown
        if dark_king_cooldown > 0:
            dark_king_cooldown -= 1

    # Dark King defeated
    if dark_king_health <= 0:

        pause()

        print("\n" + GREEN + "THE DARK KING HAS BEEN DEFEATED!" + RESET)

        pause()

        type_text("\nThe Dark King's crown falls to the floor.")

        pause()

        type_text("The darkness surrounding the castle begins to fade.")

        pause()

        type_text("You have saved the kingdom.")

        pause()

        print("\n" + YELLOW + "================================" + RESET)
        print(YELLOW + "        KINGDOM SAVED!" + RESET)
        print(YELLOW + "        YOU ARE VICTORIOUS!" + RESET)
        print(YELLOW + "================================" + RESET)

        pause()

        type_text("\nCongratulations, " + stats["character"] + "!")
        type_text("You defeated the Dark King and completed your adventure!")

        print("\nFinal Level: " + str(stats["level"]))
        print("Final Attack: " + str(stats["attack"]))
        print("Final Gold: " + YELLOW + str(stats["gold"]) + RESET)
        print("Potions Remaining: " + str(stats["potions"]))

    # Player defeated by Dark King
    elif stats["health"] <= 0:

        print("\n" + RED + "The Dark King has defeated you." + RESET)
        type_text("The kingdom remains in darkness...")


def choose_character():
    """Prompts for a character choice and returns the starting stats dict,
    or None if the player made an invalid choice."""

    type_text("\nChoose your character:\n")

    print(RED + "1. Warrior" + RESET)
    print(CYAN + "2. Wizard" + RESET)
    print(GREEN + "3. Rogue" + RESET)

    choice = input(YELLOW + "\nEnter your choice: " + RESET)

    if choice == "1":
        character = "Warrior"
        health = 120
        max_health = 120
        attack = 20
        special_attack = "Power Strike"

    elif choice == "2":
        character = "Wizard"
        health = 80
        max_health = 80
        attack = 30
        special_attack = "Fireball"

    elif choice == "3":
        character = "Rogue"
        health = 100
        max_health = 100
        attack = 25
        special_attack = "Backstab"

    else:
        print("\n" + RED + "Invalid choice." + RESET)
        return None

    return {
        "character": character,
        "health": health,
        "max_health": max_health,
        "attack": attack,
        "special_attack": special_attack,
        "gold": 50,
        "level": 1,
        "xp": 0,
        "xp_needed": 100,
        "potions": 2,
    }


def main():

    # Game title
    print(CYAN + "==============================" + RESET)
    print(CYAN + "         DARK KINGDOM" + RESET)
    print(CYAN + "==============================" + RESET)

    pause()

    # Character selection
    stats = choose_character()

    if stats is None:
        return

    # Show the player's starting information
    type_text("\nYou chose the " + stats["character"] + ".")
    pause()

    print("Health: " + GREEN + str(stats["health"]) + RESET)
    print("Gold: " + YELLOW + str(stats["gold"]) + RESET)
    print("Level: " + str(stats["level"]))
    print("Potions: " + str(stats["potions"]))
    print("Special: " + CYAN + stats["special_attack"] + RESET)

    pause()

    print("\n" + CYAN + "Your adventure begins..." + RESET)
    pause(0.5)

    # Village introduction
    type_text("\nYou arrive at a quiet village.")
    type_text("Something feels wrong.")
    pause()

    # Meet the old man
    type_text("\nAn old man approaches.")
    type_text('"The Dark King has taken the castle. Stay away from the forest."')
    pause()

    # Choose what to do in the village
    type_text("\n1. Ask about the Dark King")
    type_text("2. Head toward the forest")

    choice = input(YELLOW + "\nWhat do you do? " + RESET)

    if choice == "1":
        type_text("\nThe old man warns you that the castle is heavily guarded.")
        type_text("You thank him and head toward the forest.")

    elif choice == "2":
        type_text("\nYou leave the village and head toward the forest.")

    else:
        type_text("\nYou decide to head toward the forest.")

    # Enter the Dark Forest
    pause()

    print("\n" + CYAN + "You enter the Dark Forest..." + RESET)
    pause(0.5)

    type_text("The trees block out the sunlight.")
    type_text("Something is watching you...")
    pause(0.75)

    # First battle: Goblin
    goblin_defeated = battle_enemy(stats, "Goblin", 50, 12)

    if not goblin_defeated:
        return

    type_text("\nYou continue deeper into the forest...")
    pause()
    type_text("The sound of something large approaches.")
    pause()

    # Second battle: Werewolf
    werewolf_defeated = battle_enemy(stats, "Werewolf", 80, 16)

    if not werewolf_defeated:
        return

    type_text("\nThe forest grows silent once again...")
    pause()
    type_text("A cold wind blows through the trees...")
    pause()
    type_text("You hear the sound of armor approaching.")
    pause()

    # Third battle: Dark Knight
    dark_knight_defeated = battle_enemy(stats, "Dark Knight", 120, 20)

    if not dark_knight_defeated:
        return

    type_text("\nThe Dark Knight falls to the ground.")
    pause()
    type_text("Ahead, the Dark King's castle rises above the trees.")
    pause()

    print("\n" + CYAN + "THE CASTLE AWAITS..." + RESET)
    pause()

    type_text("\nYou enter the castle.")
    type_text("Two paths lie before you.")

    print("\n1. The Armory")
    print("2. The Dungeon")

    castle_choice = input(
        YELLOW + "\nWhich path do you take? " + RESET
    ).strip()

    if castle_choice == "2":
        room_defeated = run_castle_room_battle(stats, "Dungeon")
    else:
        # Invalid choice defaults to Armory, same as choice == "1"
        if castle_choice != "1":
            type_text("\nYou choose the Armory.")
        room_defeated = run_castle_room_battle(stats, "Armory")

    if not room_defeated:
        return

    # Castle Merchant
    run_castle_merchant(stats)

    # Approach the throne room
    type_text("\nYou continue deeper into the castle.")
    pause()
    type_text("Massive doors stand before you.")
    pause()
    type_text("You push them open.")
    pause()

    print("\n" + CYAN + "THE THRONE ROOM" + RESET)
    pause()

    type_text("\nA dark figure sits upon the throne.")
    pause()
    type_text('"So... you have made it this far."')
    pause()
    type_text('"I am the Dark King."')
    pause()

    print("\n" + RED + "THE DARK KING APPEARS!" + RESET)
    pause()

    # Dark King final boss battle
    run_dark_king_battle(stats)


if __name__ == "__main__":
    main()
