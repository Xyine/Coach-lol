import json
import os
import time


config_file = 'config.json'

with open(config_file) as f:
    config = json.load(f)

champion_name_list = config["champions"]
keep = config["keep"]


#====================================================
# UTILS VALIDATE DATASET

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


def get_unique_values_by_category(file_path):
    with open(file_path) as f:
        champions = json.load(f)

    result = {}

    for attribute in champions[0].keys():
        unique_values = set()
        for champion in champions:
            value = champion[attribute]
            if isinstance(value, list):
                unique_values.update(value)
            else:
                unique_values.add(value)
        
        result[attribute] = unique_values

    return result


def validate_data(file):
    with open(file) as f:
        champs = json.load(f)
    
    result = {}

    for champ in champs:
        missing = [info for info in keep if not champ.get(info)]
        if missing:
            result[champ["name"]] = missing

    return result


#===================================================
# UTILS CREATE AND CLEAN DATASET

def merge_dataset(files, output_file):
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

    key_mapping = {
        "positions": "lane",
        "range_type": "attackType",
        "regions": "region",
        "release_date": "releaseDate",
        "resource": "resource1"
    }

    for champ in champs:
        for target, source in key_mapping.items():
            if  not champ.get(target) and champ.get(source):
                champ[target] = champ[source]

    value_mapping = {
        "range_type": {"close": "Melee", "Ranged": "Range"},
        "resource": {"Manaless": "None"}
    }

    for champ in champs:
        for key, value in value_mapping.items():
            if not isinstance(champ[key], list):
                champ[key] = [champ[key]]
            if champ[key][0] in value:
                champ[key][0] = value[champ[key][0]]

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


def create_common_dataset(files, output_file):
    merged_file = "champs_data/merge_data.json"
    cleaned_file = "champs_data/clean_merge_data.json"
    patch_file = "champs_data/manual_fix.json"

    t0 = time.perf_counter()

    merge_dataset(files, merged_file)
    filter_common_data(merged_file)
    clean_dataset(merged_file, cleaned_file)
    patch_dataset(cleaned_file, patch_file)
    create_find_champs_dataset(cleaned_file, output_file)

    t1 = time.perf_counter()
    return f"Result available at: {output_file}\nTotal work time: {t1 - t0:.4f} seconds"


#========================================================
# USE

# print(create_common_dataset(['champs_data/champs_data_1.json', 'champs_data/champs_data_2.json', 'champs_data/champs_data_3.json'], 'champs_data/find_champs.json'))
# print(validate_data('champs_data/find_champs.json'))

