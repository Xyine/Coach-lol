from collections import Counter
import random


GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"


config_file = 'config.json'

with open(config_file) as f:
    config = json.load(f)

champion_name_list = config["champions"]

def find_the_champion_by_letter():

    champion_to_find = random.choice(champion_name_list).lower()

    while True:
        guess = input("Champion guess: ").strip().lower()

        if guess not in [c.lower() for c in champion_name_list]:
            print("You should guess an existing lol champion\n")
            continue
        elif guess != champion_to_find:
            print(f"The champion is not: {guess}")
            if len(guess) > len(champion_to_find):
                print(f"The champion name has less than {len(guess)} letters")
            elif len(guess) < len(champion_to_find):
                print(f"The champion name has more than {len(guess)} letters")
            else:
                print(f"The champion name has indeed {len(guess)} letters")

            letter_found = Counter(guess) & Counter(champion_to_find)

            if sum(letter_found.values()) == 1:
                print(f"There is a {''.join(letter_found)}\n")
            elif sum(letter_found.values()) > 1:
                print("There are " + ", ".join(f"{k} x{v}" for k, v in letter_found.items()) + "\n")
            else:
                print("None of these letter are in the champion's name\n")

        else:
            break

    print(f"Sucess the champion was: {champion_to_find}")


def format_value(val, color):
    return f"{color}{val}{RESET}"


def find_the_champ_with_info(file):
    with open(file) as f:
        champs = json.load(f)

    champions_by_name = {champ["name"].lower(): champ for champ in champs}

    champion_to_find = random.choice(champs)

    while True:
        guess = input("Champion guess: ").strip().lower()

        if guess not in champions_by_name:
            print("You should guess an existing lol champion\n")
            continue
        elif champions_by_name[guess] != champion_to_find:
            guess_info_color = ""

            for k, val_guess in champions_by_name[guess].items():
                val_target = champion_to_find[k]

                if val_guess == val_target:
                    guess_info_color += format_value(val_guess, GREEN) + " | "

                elif isinstance(val_guess, list) and isinstance(val_target, list):
                    if set(val_guess) & set(val_target):
                        guess_info_color += format_value(val_guess, YELLOW) + " | "
                    else:
                        guess_info_color += format_value(val_guess, RED) + " | "

                else:
                    guess_info_color += format_value(val_guess, RED) + " | "
            print(guess_info_color)
        else:
            break

    print(f"Sucess the champion was: {champion_to_find}")

find_the_champ_with_info('champs_data/find_champs.json')
    
