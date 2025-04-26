import re
import random
import json
import requests
from ai_config import URL, groq

def generate_QA(
                prompts: str,
                category: str = "undefined",
                path_to_qualities_json: str = "../json/qualities.json",
                path_to_animals_json: str = "../json/animals.json",
                url: str = URL,
                ai_conf: dict = groq,
                ):
    print("Start generation...")
    print("AI configures:\n")
    for i in ai_conf:
        print("\t", i, ":", ai_conf[i])
    qualities_category = "_".join([category, "qualities"])
    animals_category = "_".join([category, "animals"])
    print("Qualities category:", qualities_category)
    print("Animals category:", qualities_category)

    for prompt in prompts:
        ai_conf["MESSAGES"].append({'role' : 'user', 'content' : prompt})
        response = requests.post(url, json=ai_conf).text.replace("\\n", "\n").replace('\\"', '"')[1:-1]
        ai_conf["MESSAGES"].append({'role' : 'assistant', 'content' : response})
        print(response)
        print()
    print("Start parsing code...")
    parse_code(response)

    print("Try to get lists from parse output...")
    try:
        from output import new_qualities
    except:
        new_qualities = []
    print("New qualities list:\n", new_qualities)

    try:
         from output import new_animals
    except:
         new_animals = []
    print("New animals list:\n", new_animals)
    print()

    print(f"Read the '{path_to_animals_json}'...")
    animals = read_json(animals_category, path_to_animals_json)
    print(f"Read the '{path_to_qualities_json}'...")
    qualities = read_json(qualities_category, path_to_qualities_json)

    print("Add news:")
    add_news(animals, new_animals, animals_category)
    add_news(qualities, new_qualities, qualities_category)

    print(f"Write the '{path_to_animals_json}'...")
    write_json(animals_category, animals, path_to_animals_json)
    print(f"write the '{path_to_qualities_json}'...")
    write_json(qualities_category, qualities, path_to_qualities_json)

def get_random_item(json_file_path):
    items = set()
    with open(json_file_path, 'r') as file:
        data = json.load(file)
        for key in data:
            for item in data[key]:
                items.add(item)
    return list(items)[random.randint(0, len(items)-1)]

def add_news(items, new_items, label):
    cnt = 0
    for item in new_items:
        if item not in items:
            items.add(item)
            cnt+=1
            print("\t-", item)
    print(f"Add {cnt} new unique {label}!")

def parse_code(input_string, output="output.py"):

    # Regular expression pattern to match code blocks
    pattern = r"```python(.*?)```"

    # Find all code blocks in the input string
    code_blocks = re.findall(pattern, input_string, re.DOTALL)

    # Join the code blocks into a single string
    extracted_code = ''.join(code_blocks)

    # Write the extracted code into the output file
    with open(output, 'w') as f:
        f.write(extracted_code)

def read_json(json_key, json_file):
    """
    Reads data from a JSON file with the given key, converts it to a set, and returns it.

    Args:
        json_key (str): The top level key of the JSON file.
        json_file (str): The path to the JSON file.

    Returns:
        set: A set of data from the JSON file if the key exists, otherwise an empty set.
    """

    try:
        # Use with open context manager to read the JSON file
        with open(json_file, 'r') as file:
            # Load the JSON data from the file
            data = json.load(file)

            # Check if the json_key exists in the data
            if json_key in data:
                # Convert the data to a set and return it
                return set(data[json_key])
            else:
                # Return an empty set if the key does not exist
                return set()

    except FileNotFoundError:
        # Handle the case where the file does not exist
        print(f"The file {json_file} does not exist.")
        return set()

    except json.JSONDecodeError:
        # Handle the case where the file is not a valid JSON
        print(f"The file {json_file} is not a valid JSON.")
        return set()

def write_json(json_key: str, data: list, json_file: str):
    """
    Write data into a JSON file.

    Args:
    - json_key: The top level key of the JSON file.
    - data (iterable collection): The data to be written into the JSON file.
    - json_file: The path to the JSON file.

    Returns:
    - None
    """
    try:
        # Read all data from the JSON file as a dict
        with open(json_file, 'r') as file:
            json_data = json.load(file)
    except FileNotFoundError:
        # If the file does not exist, create a new dict
        json_data = {}
    except json.JSONDecodeError:
        # If the file is not a valid JSON, create a new dict
        json_data = {}

    # Write data into dict[json_key]
    if json_key not in json_data.keys():
        json_data[json_key] = list(data)
    else:
        data_set = set(json_data[json_key])
        for item in data: data_set.add(item)
        json_data[json_key] = list(data_set)

    # Write updated dict back to the JSON file
    with open(json_file, 'w') as file:
        json.dump(json_data, file, indent=4)
