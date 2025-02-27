import json


def modify_item_property(file_path, target_items, property_name, modifier):
    """Modifies a specific property for given items in a Pokémon drop JSON file.

    Args:
        file_path (str): Path to the JSON file.
        target_items (list): List of item names to modify.
        property_name (str): The property to change.
        modifier (function): A function that takes the current value and returns the modified value.
    """

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    pokemon_modified = 0
    total_changes = 0

    for entry in data:
        pokemon_name = entry.get("pokemon", "Unknown Pokémon")
        modified = False
        changes = 0

        if "items" in entry:
            for item in entry["items"]:
                if item["item"] in target_items and property_name in item:
                    original_value = item[property_name]
                    new_value = modifier(original_value)
                    item[property_name] = new_value
                    modified = True
                    changes += 1
                    print(
                        f"{pokemon_name}: {item['item']} - {property_name} changed from {original_value} to {new_value}")

        if modified:
            pokemon_modified += 1
            total_changes += changes
            print("-" * 50)  # Separator for clarity

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2)

    print(f"\nSuccessfully updated {property_name} for specified items!")
    print(f"Total Pokémon modified: {pokemon_modified}")
    print(f"Total values changed: {total_changes}")


if __name__ == '__main__':
    file_path = "D:\\fanclub-servers\\fanclub-pixelmon-1.16.5\\world\\datapacks\\PixelmonSlimeDrops\\data\\pixelmon\\drops\\pokedrops.json"
    target_items = ["minecraft:slime_ball", "minecraft:slime_block"]  # Items to modify
    property_name = "max"  # Property to change
    modifier = lambda x: x * 2  # Function to double the value

    modify_item_property(file_path, target_items, property_name, modifier)
