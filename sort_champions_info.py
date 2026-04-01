import json
import os


champion_name_list = [
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

keep = ["name", "gender", "positions", "species", "resource", "range_type", "regions", "release_date"]


def count_champions_in_file(file):
    with open(file) as json_data:
        champions = json.load(json_data)

    return len(champions)


def missing_champion(files):
    champions = set()
    for file in files:
        with open(file) as f:
            champs = json.load(f)
            for champ in champs:
                if champ.get("name"):
                    champions.add(champ["name"])

    full_champions = set(champion_name_list)

    return full_champions - champions


def merged_dataset(files, output_file):
    merged_data = []
    for file in files:
        try: 
            with open(file, encoding="utf-8") as f:
                champs_data = json.load(f)

                if isinstance(champs_data, list):
                    merged_data.extend(champs_data)
                else:
                    print(f"Warning {file} is not a list")
        except Exception as e:
            print(f"Error reading {file}: {e}")
    
    if os.path.exists(output_file):
        print(f"Warning: {output_file} will be overwritten")

    with open(output_file, 'w', encoding="utf-8") as f:
        json.dump(merged_data, f, indent=4)


def merge_dict_with_rename(d1, d2):
    result = d1.copy()

    for k, v in d2.items():
        if k not in result:
            result[k] = v
        else:
            i = 1
            new_key = f"{k}{i}"
            while new_key in result:
                i += 1
                new_key = f"{k}{i}"
            result[new_key] = v

    return result


def filter_common_data(file):
    with open(file) as f:
        champs = json.load(f)

    merged = {}

    for champ in champs:
        name = champ.get("name")
        if not name:
            continue
        
        if name not in merged:
            merged[name] = champ
        else:
            merged[name] = merge_dict_with_rename(merged[name] , champ)

    result = list(merged.values())

    with open(file, 'w', encoding="utf-8") as f:
        json.dump(result, f, indent=4)


def clean_dataset(input_file, output_file):
    with open(input_file) as f:
        champs = json.load(f)

    mapping = {
        "positions": "lane",
        "range_type": "attackType",
        "regions": "region",
        "release_date": "releaseDate",
        "resource": "resource1"
    }

    for champ in champs:
        for target, source in mapping.items():
            if  not champ.get(target) and champ.get(source):
                champ[target] = champ[source]

    with open(output_file, 'w', encoding="utf-8") as f:
        json.dump(champs, f, indent=4)


def patch_dataset(dataset, patch_dataset):
    with open(dataset) as f:
        champs = json.load(f)
    with open(patch_dataset) as f:
        fix = json.load(f)

    for champ in champs:
        name = champ.get("name")
        if name in fix:
            champ.update(fix[name])

    with open(dataset, 'w') as f:
        json.dump(champs, f, indent=4)


def create_find_champs_dataset(input_file, output_file):
    with open(input_file) as f:
        champs = json.load(f)

    result = [
        {k: v for k, v in champ.items() if k in keep}
        for champ in champs
    ]

    with open(output_file, 'w', encoding="utf-8") as f:
        json.dump(result, f, indent=4)


def validate_data(file):
    with open(file) as f:
        champs = json.load(f)
    
    result = {}

    for champ in champs:
        missing = [info for info in keep if not champ.get(info)]
        if missing:
            result[champ["name"]] = missing

    return result

# clean_dataset('champs_data/merge_champs.json', 'champs_data/clean_merge_champs.json')
# patch_dataset('champs_data/clean_merge_champs.json', 'champs_data/manual_fix.json')
# create_find_champs_dataset('champs_data/clean_merge_champs.json', 'champs_data/find_champs.json')
# print(validate_data('champs_data/find_champs.json'))

# create_find_champs_dataset('champs_data/merge_champs.json', 'champs_data/find_champs.json')

# merged_dataset(["champs_data/champions.json", "champs_data/find_champs.json", "champs_data/find-champ-data.json"], 'champs_data/merge_champs.json')
# print(count_champions_in_file('champs_data/merge_champs.json'))
# filter_common_data('champs_data/merge_champs.json')
# print(count_champions_in_file('champs_data/merge_champs.json'))


def create_common_dataset(files):
    return


# print(missing_champion(["champs_data/champions.json", "champs_data/find_champs.json", "champs_data/find-champ-data.json"]))

# print(count_champions_in_file("champs_data/champions.json"))
# print(count_champions_in_file("champs_data/loldle_champs.json"))
# print(count_champions_in_file("champs_data/loldle-champ-data.json"))

