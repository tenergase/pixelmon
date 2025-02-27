import nbtlib
import os


def remove_tag(pokemon_data, tag_name, location, filename):
    """Remove the specified tag from a Pokémon if it exists and print its contents."""
    if tag_name in pokemon_data:
        del pokemon_data[tag_name]
        print(f"  Removed '{tag_name}' in {location} of {filename}: {pokemon_data[tag_name]}")


def scan_folder_for_tag_to_delete(folder_path, tag_name):
    """Scan all .pk and .comp files in the given folder and remove the specified tag."""
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Process .pk files (party Pokémon)
        if filename.endswith(".pk"):
            print(f"Processing: {filename}")

            try:
                pokemon_file = nbtlib.load(file_path)

                # Dynamically find all party Pokémon
                for tag in list(pokemon_file.keys()):
                    if tag.startswith("party"):  # Ensure it's a party slot
                        remove_tag(pokemon_file[tag], tag_name, tag, filename)

                # Save the modified file
                pokemon_file.save(file_path)
                print(f"  Saved changes to {filename}.\n")

            except Exception as e:
                print(f"  Error processing {filename}: {e}\n")

        # Process .comp files (PC Pokémon storage)
        elif filename.endswith(".comp"):
            print(f"Processing: {filename}")

            try:
                pokemon_file = nbtlib.load(file_path)

                # Dynamically find all boxes
                for box_tag in list(pokemon_file.keys()):
                    if box_tag.startswith("BoxNumber"):  # Ensure it's a box entry
                        box_data = pokemon_file[box_tag]

                        # Iterate through all Pokémon in the box
                        for pc_key in list(box_data.keys()):
                            if pc_key.startswith("pc"):  # Ensure it's a Pokémon entry
                                remove_tag(box_data[pc_key], tag_name, f"{pc_key} in {box_tag}", filename)

                # Save the modified file
                pokemon_file.save(file_path)
                print(f"  Saved changes to {filename}.\n")

            except Exception as e:
                print(f"  Error processing {filename}: {e}\n")


if __name__ == '__main__':
    folder_path = "D:\\fanclub-servers\\fanclub-pixelmon-1.16.5\\world\\data\\pokemon"
    tag_to_delete = "Size"
    scan_folder_for_tag_to_delete(folder_path, tag_to_delete)
    print("Batch processing complete!")

# 1.16.5 -> 1.20.2
# pokerus tag not present by default in old versions
# always present in new versions
