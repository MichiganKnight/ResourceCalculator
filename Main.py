import os
import Buildings
import Troops
import Abilities

def get_game_choice() -> str:
    print("\n--- Select Game ---")
    print("1. Clash of Clans")
    print("2. Boom Beach")

    while True:
        choice = input("Enter Game Choice (1, 2) or 'Q' to Quit: ").strip().lower()
        if choice in ['1', '2', 'q']:
            return choice

        print("Invalid Choice - Please Enter 1, 2, or 'Q'")

def main():
    if not os.path.exists("Data"):
        print("Note: 'Data/' File Module Tree Not Detected - Operations Will Default to Manual Parsing")

    while True:
        game_choice = get_game_choice()
        if game_choice == 'q':
            print("Exiting Resource Calculator...")
            break

        print("\n--- Select Target Category Module ---")
        print("1. Buildings")
        print("2. Troops")
        print("3. Abilities / Weaponry Spells")
        print("4. Dynamic Discovery (Browse All JSON Modules)")

        while True:
            category_choice = input("Enter Choice (1-4): ").strip()
            if category_choice in ['1', '2', '3', '4']:
                break
            print("Invalid Choice - Select a Module Layout Between 1 and 4")

        if category_choice == '1':
            Buildings.handle_buildings(game_choice)
        elif category_choice == '2':
            Troops.handle_troops(game_choice)
        elif category_choice == '3':
            Abilities.handle_abilities(game_choice)
        elif category_choice == '4':
            from Calculator_Engine import run_calculator_flow
            if game_choice == '1':
                run_calculator_flow("Clash of Clans", "ClashOfClans", ["Gold", "Elixir", "Dark Elixir"], allow_time_savers=False)
            elif game_choice == '2':
                run_calculator_flow("Boom Beach", "BoomBeach", ["Gold", "Wood", "Stone", "Iron"], allow_time_savers=True)

if __name__ == "__main__":
    main()