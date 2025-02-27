import nbtlib
import os
import random


def add_growth_tag(pokemon_data, location, filename):
    """Add a 'Growth' tag to a Pokémon if it does not already have it."""
    if "Growth" not in pokemon_data:
        # Define the probabilities and corresponding values for the Growth tag
        growth_values = [0, 1, 2, 3, 4, 5, 6]
        growth_probabilities = [0.05, 0.10, 0.20, 0.30, 0.20, 0.10, 0.05]

        # Select a value based on the defined probabilities
        growth_value = random.choices(growth_values, growth_probabilities)[0]

        # Add the Growth tag
        pokemon_data["Growth"] = nbtlib.Byte(growth_value)
        print(f"  Added 'Growth' tag with value {growth_value} to {location} of {filename}.")


def scan_folder_and_add_growth(folder_path):
    """Scan all .pk and .comp files in the folder and add the 'Growth' tag if missing."""
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
                        add_growth_tag(pokemon_file[tag], tag, filename)

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
                                add_growth_tag(box_data[pc_key], f"{pc_key} in {box_tag}", filename)

                # Save the modified file
                pokemon_file.save(file_path)
                print(f"  Saved changes to {filename}.\n")

            except Exception as e:
                print(f"  Error processing {filename}: {e}\n")


if __name__ == '__main__':
    folder_path = "D:\\fanclub-servers\\fanclub-pixelmon-1.16.5\\world\\data\\pokemon"  # Assigned folder path
    scan_folder_and_add_growth(folder_path)
    print("Batch processing complete!")

# 1.16.5
# requires growth tag for stats page