from collections import Counter
import random


def find_the_champion():
    champion_list = [
        "Aatrox", "Ahri", "Akali", "Akshan", "Alistar", "Ambessa", "Amumu", "Anivia", "Annie", "Aphelios", "Ashe", "Aurelion Sol", 
        "Aurora", "Azir", "Bard", "Bel'Veth", "Blitzcrank", "Brand", "Braum", "Briar", "Caitlyn", "Camille", "Cassiopeia", "Cho'Gath", 
        "Corki", "Darius", "Diana", "Dr. Mundo", "Draven", "Ekko", "Elise", "Evelynn", "Ezreal", "Fiddlesticks", "Fiora", "Fizz", 
        "Galio", "Gangplank", "Garen", "Gnar", "Gragas", "Graves", "Gwen", "Hecarim", "Heimerdinger", "Hwei", "Illaoi", "Irelia", 
        "Ivern", "Janna", "Jarvan IV", "Jax", "Jayce", "Jhin", "Jinx", "Kai'Sa", "Kalista", "Karma", "Karthus", "Kassadin", "Katarina", 
        "Kayle", "Kayn", "Kennen", "Kha'Zix", "Kindred", "Kled", "Kog'Maw", "K'Sante", "LeBlanc", "Lee Sin", "Leona", "Lillia", 
        "Lissandra", "Lucian", "Lulu", "Lux", "Malphite", "Malzahar", "Maokai", "Master Yi", "Mel", "Milio", "Miss Fortune", 
        "Mordekaiser", "Morgana", "Naafiri", "Nami", "Nasus", "Nautilus", "Neeko", "Nidalee", "Nilah", "Nocturne", "Nunu & Willump", 
        "Olaf", "Orianna", "Ornn", "Pantheon", "Poppy", "Pyke", "Qiyana", "Quinn", "Rakan", "Rammus", "Rek'Sai", "Rell", 
        "Renata Glasc", "Renekton", "Rengar", "Riven", "Rumble", "Ryze", "Samira", "Sejuani", "Senna", "Seraphine", "Sett", "Shaco", 
        "Shen", "Shyvana", "Singed", "Sion", "Sivir", "Skarner", "Smolder", "Sona", "Soraka", "Swain", "Sylas", "Syndra", "Tahm Kench", 
        "Taliyah", "Talon", "Taric", "Teemo", "Thresh", "Tristana", "Trundle", "Tryndamere", "Twisted Fate", "Twitch", "Udyr", "Urgot", 
        "Varus", "Vayne", "Veigar", "Vel'Koz", "Vex", "Vi", "Viego", "Viktor", "Vladimir", "Volibear", "Warwick", "Wukong", "Xayah", 
        "Xerath", "Xin Zhao", "Yasuo", "Yone", "Yorick", "Yunara", "Yuumi", "Zaahen", "Zac", "Zed", "Zeri", "Ziggs", "Zilean", "Zoe", 
        "Zyra"
    ]

    champion_to_find = random.choice(champion_list).lower()

    while True:
        guess = input("Champion guess: ").strip().lower()

        if guess not in [c.lower() for c in champion_list]:
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


find_the_champion()
