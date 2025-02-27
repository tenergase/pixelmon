import nbtlib
import os


def search_pokemon_by_tag(folder_path, tag_name, find_with_tag=True):
    """Search for Pokémon that either contain or do not contain a specified tag."""
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Process .pk files (party Pokémon)
        if filename.endswith(".pk"):
            print(f"Processing: {filename}")

            try:
                pokemon_file = nbtlib.load(file_path)

                # Find and filter the Pokémon based on the tag
                filtered_pokemon = []
                for tag in list(pokemon_file.keys()):
                    if tag.startswith("party"):  # Ensure it's a party slot
                        if (find_with_tag and tag_name in pokemon_file[tag]) or (not find_with_tag and tag_name not in pokemon_file[tag]):
                            filtered_pokemon.append((tag, pokemon_file[tag]))

                # Sort Pokémon by their tag number
                filtered_pokemon.sort(key=lambda x: int(x[0].replace('party', '')))

                # Print results
                for tag, data in filtered_pokemon:
                    print(f"  Found Pokémon in {tag} - {tag_name}: {data[tag_name] if tag_name in data else 'Not present'}")

            except Exception as e:
                print(f"  Error processing {filename}: {e}\n")

        # Process .comp files (PC Pokémon storage)
        elif filename.endswith(".comp"):
            print(f"Processing: {filename}")

            try:
                pokemon_file = nbtlib.load(file_path)

                # Find and filter the Pokémon based on the tag
                filtered_pokemon = []
                for box_tag in list(pokemon_file.keys()):
                    if box_tag.startswith("BoxNumber"):  # Ensure it's a box entry
                        box_data = pokemon_file[box_tag]
                        for pc_key in list(box_data.keys()):
                            if pc_key.startswith("pc"):  # Ensure it's a Pokémon entry
                                if (find_with_tag and tag_name in box_data[pc_key]) or (not find_with_tag and tag_name not in box_data[pc_key]):
                                    filtered_pokemon.append((pc_key, box_data[pc_key]))

                # Sort Pokémon by their tag number
                filtered_pokemon.sort(key=lambda x: int(x[0].replace('pc', '')))

                # Print results
                for pc_key, data in filtered_pokemon:
                    print(f"  Found Pokémon in {pc_key} - {tag_name}: {data[tag_name] if tag_name in data else 'Not present'}")

            except Exception as e:
                print(f"  Error processing {filename}: {e}\n")


if __name__ == '__main__':
    folder_path = "D:\\fanclub-servers\\fanclub-pixelmon-1.16.5\\world\\data\\pokemon"  # Folder path
    tag_name = "Growth"  # Specify the tag you want to search for
    find_with_tag = True  # Set to True if you want to find Pokémon that have the tag
    search_pokemon_by_tag(folder_path, tag_name, find_with_tag)
    print("Tag search complete!")

# 1.16.5 -> 1.20.2
# Growth -> Size
# Pokerus
# Nickname -> FormattedNickname
