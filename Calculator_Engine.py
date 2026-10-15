import os
import json
from typing import List, Dict, Tuple
from Utils import get_non_negative_integer, calculate_wait_time, format_hours

BASE_DATA_DIR = "Data"

def get_categories_for_game(game_folder: str) -> List[str]:
    """
    Scans Game Directory and Returns Categories Based on Available JSON Files
    :param game_folder: The Game Folder to Scan
    :return: List of Categories
    """
    game_path = os.path.join(BASE_DATA_DIR, game_folder)
    if not os.path.isdir(game_path):
        return []

    return sorted([os.path.splitext(file)[0] for file in os.listdir(game_path) if file.lower().endswith(".json")])

def load_category_data(game_folder: str, category: str) -> Dict:
    """
    Loads a Specific JSON Category File Dynamically
    :param game_folder: The Game Folder
    :param category: The Category Name
    :return: Dictionary of Data
    """
    filepath = os.path.join(BASE_DATA_DIR, game_folder, f"{category}.json")
    try:
        with open(filepath, "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error Loading {filepath}: {e}")
        return {}

def select_upgrade_by_category(game_folder: str, specific_category: str = None) -> Tuple[str, Dict]:
    """
    Guides User Dynamically Through Item and Level Selection
    :param game_folder: The Game Folder
    :param specific_category: The Specific Category to Select from
    :return: Tuple of Item Name and Level Costs/Data
    """
    if specific_category:
        selected_category = specific_category
    else:
        categories = get_categories_for_game(game_folder)
        if not categories:
            print(f"No JSON Data Modules Found in '{os.path.join(BASE_DATA_DIR, game_folder)}'")
            return "", {}

        print("\nSelect Category:")
        for index, category in enumerate(categories, 1):
            print(f"{index}. {category}")

        category_choice = get_non_negative_integer("Choice #: ") - 1
        if category_choice < 0 or category_choice >= len(categories):
            print("Invalid Category Selection")
            return "", {}
        selected_category = categories[category_choice]

    items_dict = load_category_data(game_folder, selected_category)
    if not items_dict:
        print(f"The Module Entry File '{selected_category}.json' is Empty or Missing'")
        return "", {}

    items = sorted(list(items_dict.keys()))
    print(f"\n Select Item from {selected_category}:")
    for index, item in enumerate(items, 1):
        print(f"{index}. {item}")

    item_choice = get_non_negative_integer("Choice #: ") - 1
    if item_choice < 0 or item_choice >= len(items):
        print("Invalid Item Selection")
        return "", {}

    selected_item = items[item_choice]
    levels_dict = items_dict[selected_item]

    levels = sorted(list(levels_dict.keys()), key=lambda x: int(x) if x.isdigit() else x)
    print(f"\nSelect Target Level for {selected_item}:")
    for index, level in enumerate(levels, 1):
        print(f"{index}. {level}")

    level_choice = get_non_negative_integer("Choice #: ") - 1
    if level_choice < 0 or level_choice >= len(levels):
        print("Invalid Level Selection")
        return "", {}

    selected_level = levels[level_choice]

    return f"{selected_item} (Level {selected_level})", levels_dict[selected_level]

def run_calculator_flow(game_name: str, game_folder: str, resources: list, forced_category: str = None, allow_time_savers: bool = False):
    """
    Runs the Calculator Flow
    :param game_name: The Game Name
    :param game_folder: The Game Folder
    :param resources: Resources to Calculate
    :param forced_category: The Specific Category to Select
    :param allow_time_savers: If Time Savers are Allowed
    """
    print(f"\n======================================")
    print(f"       {game_name} Calculator")
    print(f"======================================")

    upgrade_data = {}
    current_inventory = {}
    production_rates = {}
    missing_resources = {}
    target_name = "Manual Entry"
    use_manual = True
    base_upgrade_time = 0.0

    target_path = os.path.join(BASE_DATA_DIR, game_folder)
    if os.path.exists(target_path):
        prompt_message = f"Load Configuration Dynamically from Registry? (Y/N): " if not forced_category else f"Load Directly from {forced_category}.json Module? (Y/N): "
        use_db = input(prompt_message).strip().lower()
        if use_db == "y":
            target_name, upgrade_data = select_upgrade_by_category(game_folder, forced_category)
            if upgrade_data:
                use_manual = False
                print(f"\nSelected Profile Target: {target_name}")
            else:
                print("Falling Back to Manual Entry Mode")

    # If loading from database, extract the upgrade duration from the dict if it exists
    if not use_manual:
        # Using .pop() removes "Time" from upgrade_data so it won't trigger resource calculation errors
        base_upgrade_time = float(upgrade_data.pop("Time", 0.0))

    print("\n--- Step 1: Resource Requirements ---")
    for resource in resources:
        if use_manual:
            upgrade_data[resource] = get_non_negative_integer(f"Enter Required {resource} Amount: ")
        else:
            upgrade_data[resource] = upgrade_data.get(resource, 0)
            print(f"Required {resource}: (Auto-Filled): {upgrade_data[resource]:,}")

        current_inventory[resource] = get_non_negative_integer(f"How Much {resource} Do You Have?: ")
        missing_resources[resource] = max(0, upgrade_data[resource] - current_inventory[resource])

    print("\n--- Step 2: Hourly Production Rates ---")
    needs_farming = False
    for resource in resources:
        if missing_resources[resource] > 0:
            production_rates[resource] = get_non_negative_integer(f"Enter Your Hourly Production Rate for {resource}: ")
            needs_farming = True
        else:
            production_rates[resource] = 0

    print("\n================ TOTAL ASSESSMENT ================")
    if not use_manual:
        print(f"Target Upgrade  : {target_name}")
        if base_upgrade_time > 0:
            print(f"In-Game Build Time: {format_hours(base_upgrade_time)}")

    for resource in resources:
        if missing_resources[resource] > 0:
            print(f"-> Missing {resource}: {missing_resources[resource]:,}")
        else:
            print(f"-> {resource}: Sufficient (Surplus: {current_inventory[resource] - upgrade_data[resource]:,})")

    # Step 3: Farming Wait Time Projections
    if needs_farming:
        base_hours_needed = calculate_wait_time(missing_resources, production_rates)
        print(f"\nEstimated Passive Farming Wait Time: {format_hours(base_hours_needed)}")
    else:
        print("\n🎉 Upgrades Ready! You Possess Sufficient Stocks to Proceed Immediately.")

    # Step 4: Upgrade Construction/Research Timer Projections
    if base_upgrade_time > 0:
        print(f"\n--- Step 4: Upgrade Timer Assessment ---")
        if allow_time_savers:
            use_savers = input("Apply 15-Minute Time Savers to Shorten the Upgrade Build Time? (Y/N): ").strip().lower()
            if use_savers == "y":
                num_savers = get_non_negative_integer("Enter Number of 15-Minute Time Savers to Apply: ")
                savers_in_hours = (num_savers * 15) / 60
                adjusted_build_time = max(0.0, base_upgrade_time - savers_in_hours)

                print(f"\n--- Upgrade Build Timer Projections ---")
                print(f"Applied {num_savers} Savers (-{savers_in_hours:.2f} Hours)")
                print(f"Original Upgrade Duration : {format_hours(base_upgrade_time)}")
                print(f"Adjusted Upgrade Duration : {format_hours(adjusted_build_time)}")
            else:
                print(f"Standard Upgrade Duration: {format_hours(base_upgrade_time)}")
        else:
            print(f"Standard Upgrade Duration: {format_hours(base_upgrade_time)}")