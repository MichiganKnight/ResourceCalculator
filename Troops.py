from Calculator_Engine import run_calculator_flow

def handle_troops(game_choice: str):
    if game_choice == '1':
        run_calculator_flow("Clash of Clans", "ClashOfClans", ["Gold", "Elixir", "Dark Elixir"], forced_category="Troops", allow_time_savers=False)
    elif game_choice == '2':
        run_calculator_flow("Boom Beach", "BoomBeach", ["Gold", "Wood", "Stone", "Iron"], forced_category="Troops", allow_time_savers=True)