
import random


def start_new_game():
    city_size_restrictions = {"min": 4, "max": 8}
    city_size_restrictions["city_sizes"] = [str(i).zfill(0) for i in range(city_size_restrictions["min"], city_size_restrictions["max"] + 1)]
    all_letter_display_pairs = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H"}
    all_letter_input_pairs = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

    city_size = city_size_selection(city_size_restrictions)
    board_metadata = generate_board_metadata(city_size, all_letter_display_pairs, all_letter_input_pairs)

    buildings_tracker = generate_initial_buildings(city_size)
    board_tracker = generate_new_board(city_size)

    current_turn = 0

    run_game(board_tracker, buildings_tracker, current_turn, board_metadata)

    return {}


def run_game(board_tracker, buildings_tracker, current_turn, board_metadata):
    proceed_next_turn = True
    while current_turn < board_metadata["total_turns"]:
        if proceed_next_turn is True:
            current_turn += 1
            building_options = get_random_buildings(buildings_tracker)

        print("\nTurn", current_turn)
        display_board(board_tracker, buildings_tracker, board_metadata)
        display_game_menu(building_options)
        return_values = game_menu_option_selection(board_tracker, buildings_tracker, building_options, current_turn, board_metadata)

        if "exit" in return_values:
            if return_values["exit"] is True:
                return {}

        if "err" in return_values:
            print(return_values["err"])

        if "updated_board_tracker" in return_values:
            board_tracker = return_values["updated_board_tracker"]

        if "updated_buildings_tracker" in return_values:
            buildings_tracker = return_values["updated_buildings_tracker"]

        if return_values["proceed_next_turn"] is True:
            proceed_next_turn = True
        else:
            proceed_next_turn = False

    return {}


def city_size_selection(city_size_restrictions):
    while True:
        user_input = input("Enter city size (min {}, max {}): ".format(city_size_restrictions["min"], city_size_restrictions["max"]))
        if user_input in city_size_restrictions["city_sizes"]:
            return int(user_input)
        else:
            print("Invalid city size, try again")


def generate_board_metadata(city_size, all_letter_display_pairs, all_letter_input_pairs):
    assert type(city_size) == int, "city_size not of type 'int'"

    letter_display_pairs = {i: all_letter_display_pairs[i] for i in range(city_size)}
    letter_input_pairs = {list(all_letter_input_pairs)[i]: i for i in range(city_size)}
    total_turns = city_size * city_size

    metadata = {"total_turns": total_turns, "letter_display_pairs": letter_display_pairs, "letter_input_pairs": letter_input_pairs}

    return metadata


def generate_initial_buildings(city_size):
    assert len(building_pool) > 0, "building pool empty"
    assert type(city_size) == int, "city_size not of type 'int'"

    max_buildings = city_size * 2
    buildings = {}
    for b in building_pool:
        buildings[b] = max_buildings

    return buildings


def generate_new_board(city_size):
    assert type(city_size) == int, "city_size not of type 'int'"

    board = [["" for i in range(city_size)] for i in range(city_size)]
    return board


def get_random_buildings(buildings_tracker):
    buildings = []

    for i in range(2):
        available_buildings = []
        for key in buildings_tracker:
            if buildings_tracker[key] > 0:
                available_buildings.append(key)

        index = random.randint(0, len(available_buildings) - 1)
        buildings.append(available_buildings[index])

    return buildings


def display_board(board_tracker, buildings_tracker, board_metadata):
    letters = board_metadata["letter_display_pairs"]
    size = len(board_tracker)
    row_divider = "  " + "+-----" * size + "+"

    print("   ", end="")
    for col in range(size):
        print("  " + letters[col] + "   ", end="")
    print("   Remaining buildings")

    buildings_index_count = 0

    for row_index, row_value in enumerate(board_tracker, start=1):
        if row_index == 1:
            print(row_divider + "   -------------------")
        elif buildings_index_count < len(buildings_tracker):
            building = list(buildings_tracker)[buildings_index_count]
            building_count = buildings_tracker[building]
            print("{}   {}: {}".format(row_divider, building, building_count))
            buildings_index_count += 1
        else:
            print(row_divider)

        print(" {}|".format(row_index), end="")
        for cell in row_value:
            if cell == "":
                print("     |", end="")
            else:
                print(" " + cell + " |", end="")

        if buildings_index_count < len(buildings_tracker):
            building = list(buildings_tracker)[buildings_index_count]
            building_count = buildings_tracker[building]
            print("   {}: {}".format(building, building_count))
            buildings_index_count += 1
        else:
            print()

    print(row_divider)


def display_game_menu(building_options):
    print("1. Build a", building_options[0])
    print("2. Build a", building_options[1])
    print("3. See current score")
    print("\n4. Save game")
    print("0. Exit to main menu")


def game_menu_option_selection(board_tracker, buildings_tracker, building_options, current_turn, board_metadata):
    main_menu_options = {"0": exit_game_menu,
                         "1": build_building,
                         "2": build_building,
                         "3": see_current_score,
                         "4": save_game}

    user_input = input("Your choice? ")

    if user_input in list(main_menu_options.keys()):
        if user_input == "1" or user_input == "2":
            return main_menu_options[user_input](board_tracker, buildings_tracker, building_options[int(user_input) - 1], current_turn, board_metadata)
        else:
            return main_menu_options[user_input]()

    else:
        return {"err": "Invalid option, try again", "proceed_next_turn": False}


def exit_game_menu():
    return {"exit": True}


def build_building(board_tracker, buildings_tracker, building, current_turn, board_metadata):
    print("build_building")
    return {"proceed_next_turn": False}


def see_current_score():
    print("see_current_score")
    return {"proceed_next_turn": False}


def save_game():
    return {"proceed_next_turn": False}


def load_saved_game():
    print("load saved game")
    return {}


def choose_building_pool():
    return{}


def show_high_scores():
    return {}


def display_main_menu():
    print("\nWelcome, mayor of Simp City!")
    print("------------------------------")
    print("1. Start new game")
    print("2. Load saved game")
    print("3. Choose building pool")
    print("4. Show high scores")
    print("\n0. Exit")


def main_menu_option_selection():
    main_menu_options = {"0": exit_main_menu,
                         "1": start_new_game,
                         "2": load_saved_game,
                         "3": choose_building_pool,
                         "4": show_high_scores}

    user_input = input("Your choice? ")

    if user_input in list(main_menu_options.keys()):
        return_values = main_menu_options[user_input]()

        if "exit" in return_values:
            if return_values["exit"] is True:
                return {"exit": True}

        if "bp" in return_values:
            return {"bp": return_values["bp"]}

    else:
        return {"err": "invalid option, try again"}

    return {}


def exit_main_menu():
    return {"exit": True}


global building_pool
building_pool = ["BCH", "FAC", "HSE", "SHP", "HWY"]


def master_loop():
    main_running = True
    while main_running:
        display_main_menu()
        return_values = main_menu_option_selection()

        if "exit" in return_values:
            if return_values["exit"] is True:
                main_running = False

        if "err" in return_values:
            print(return_values["err"])

        if "bp" in return_values:
            global building_pool
            building_pool = return_values["bp"]


if __name__ == "__main__":
    master_loop()
