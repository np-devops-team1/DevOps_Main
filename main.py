
import random
import sys


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
        elif user_input == "3":
            return main_menu_options[user_input](board_tracker)
        else:
            return main_menu_options[user_input]()

    else:
        return {"err": "Invalid option, try again", "proceed_next_turn": False}


def exit_game_menu():
    return {"exit": True}


def build_building(board_tracker, buildings_tracker, building, current_turn, board_metadata):
    return_values = select_building_location(board_tracker, current_turn, board_metadata)

    if "exit" in return_values:
        if return_values["exit"] is True:
            return {"proceed_next_turn": False}

    if "err" in return_values:
        return {"proceed_next_turn": False, "err": return_values["err"]}

    if "building_coordinates" in return_values:
        updated_board_tracker = add_building_to_board(board_tracker, building, return_values["building_coordinates"])
        updated_buildings_tracker = update_buildings_tracker(buildings_tracker, building)
        return {"proceed_next_turn": True, "updated_board_tracker": updated_board_tracker, "updated_buildings_tracker": updated_buildings_tracker}

    return {"proceed_next_turn": False, "err": "Error in selecting building location"}


def select_building_location(board_tracker, current_turn, board_metadata):
    letters = board_metadata["letter_input_pairs"]

    while True:
        user_input = input("Build where? ")
        if user_input == "0":
            return {"exit": True}

        building_location = {"col": user_input[0], "row": user_input[1:]}

        if building_location["col"] in letters and building_location["row"] in [str(i).zfill(0) for i in range(1, len(letters) + 1)]:
            building_coordinates = {}
            building_coordinates["col"] = letters[building_location["col"]]
            building_coordinates["row"] = int(building_location["row"]) - 1

            if current_turn == 1:
                return {"building_coordinates": building_coordinates}
            else:
                if check_location_occupied(board_tracker, building_coordinates) is False:
                    if check_adjacent_location_occupied(board_tracker, building_coordinates) is True:
                        return {"building_coordinates": building_coordinates}
                    else:
                        print("You must build next to an existing building")
                else:
                    print("You must build on an empty location")
        else:
            print("Location not found")


def check_location_occupied(board_tracker, building_coordinates):
    if board_tracker[building_coordinates["row"]][building_coordinates["col"]] != "":
        return True
    else:
        return False


def check_adjacent_location_occupied(board_tracker, building_coordinates):
    if building_coordinates["row"] > 0:
        if board_tracker[building_coordinates["row"] - 1][building_coordinates["col"]] != "":  # Check top
            return True

    if building_coordinates["row"] < len(board_tracker) - 1:
        if board_tracker[building_coordinates["row"] + 1][building_coordinates["col"]] != "":  # Check bottom
            return True

    if building_coordinates["col"] > 0:
        if board_tracker[building_coordinates["row"]][building_coordinates["col"] - 1] != "":  # Check left
            return True

    if building_coordinates["col"] < len(board_tracker) - 1:
        if board_tracker[building_coordinates["row"]][building_coordinates["col"] + 1] != "":  # Check right
            return True

    return False


def add_building_to_board(board_tracker, building, building_coordinates):
    board_tracker[building_coordinates["row"]][building_coordinates["col"]] = building
    return board_tracker


def update_buildings_tracker(buildings_tracker, building):
    buildings_tracker[building] -= 1
    return buildings_tracker


def calculate_bch_score(buildings_tracker):
    bch_score = 0
    all_bch_score = []
    for building_row in buildings_tracker:
        for building_column in range(0, len(building_row)):
            if building_row[building_column] == "BCH":
                if building_column == 0 or building_column == len(building_row) - 1:
                    bch_score = bch_score + 3
                    all_bch_score.append(3)
                else:
                    bch_score = bch_score + 1
                    all_bch_score.append(1)

    return bch_score, all_bch_score


def calculate_fac_score(buildings_tracker):
    fac_score = 0
    no_of_fac = 0
    all_fac_score = []
    for building_row in buildings_tracker:
        for building_column in range(0, len(building_row)):
            if building_row[building_column] == "FAC":
                no_of_fac = no_of_fac + 1

    if no_of_fac < 5:
        all_fac_score = [no_of_fac for i in range(no_of_fac)]
        fac_score = no_of_fac * no_of_fac
    else:
        no_of_fac = no_of_fac - 4
        all_fac_score = [4 for i in range(4)]
        all_fac_score.append([1 for i in range(no_of_fac)])
        fac_score = no_of_fac + (4 * 4)
    return fac_score, all_fac_score


def calculate_shp_score(buildings_tracker):
    shp_score = 0
    all_shp_score = []

    for building_row in range(0, len(buildings_tracker)):
        for building_column in range(0, len(buildings_tracker[building_row])):
            build = buildings_tracker[building_row][building_column]

            if build == "SHP":
                # get adjacent building of a plot

                score = 0
                buildingCounter = {"FAC": 0, "BCH": 0,
                                   "SHP": 0, "HSE": 0, "HWY": 0, "PRK": 0, "MON": 0}
                adjacent_building = get_adjacent_buildings(
                    building_row, building_column, buildings_tracker)

                for building in adjacent_building:
                    if building in buildingCounter.keys():
                        if buildingCounter.get(building) == 0:
                            score = score + 1
                            buildingCounter[building] = 1

                shp_score = shp_score + score
                all_shp_score.append(score)
    return shp_score, all_shp_score


hse_scoring_builts = {"FAC": 1, "BCH": 2, "HSE": 1, "SHP": 1, "HWY": 0, "MON": 1, "PRK": 1, "": 0}


def calculate_hse_score(buildings_tracker):
    hse_score = 0
    all_hse_score = []

    for building_row in range(0, len(buildings_tracker)):
        for building_column in range(0, len(buildings_tracker[building_row])):
            build = buildings_tracker[building_row][building_column]

            if build == "HSE":
                score = 0
                adjacent_building = get_adjacent_buildings(
                    building_row, building_column, buildings_tracker)

                for building in adjacent_building:
                    score = score + hse_scoring_builts.get(building)
                all_hse_score.append(score)
                hse_score = hse_score + score
    return hse_score, all_hse_score


def calculate_hwy_score(buildings_tracker):
    hwy_score = 0
    all_hwy_score = []

    for building_row in range(0, len(buildings_tracker)):
        for building_column in range(0, len(buildings_tracker[building_row])):
            build = buildings_tracker[building_row][building_column]

            if build == "HWY":
                score = 0
                # Find the number of rows
                for i in range(building_column, len(buildings_tracker[building_row])):
                    if buildings_tracker[building_row][i] == "HWY":
                        score = score + 1
                    else:
                        break
                for i in reversed(range(0, building_column)):
                    if buildings_tracker[building_row][i] == "HWY":
                        score = score + 1
                    else:
                        break
                hwy_score = hwy_score + score
                all_hwy_score.append(score)
    return hwy_score, all_hwy_score


visited = []  # Set to keep track of visited nodes of PRK
global_visited = []
prk_score_dic = {"1": 1, "2": 3, "3": 8, "4": 16, "5": 22, "6": 23, "7": 24, "8": 25}


def calculate_prk_score(buildings_tracker):
    prk_score = 0
    prk_history = []

    for building_row in range(0, len(buildings_tracker)):
        for building_column in range(0, len(buildings_tracker[building_row])):
            build = buildings_tracker[building_row][building_column]

            if build == "PRK":
                if ([building_row, building_column]) not in global_visited:
                    # Find the number of rows
                    visited = []
                    prk_score = prk_score + prk_score_dic.get(str(dfs(visited, buildings_tracker, [building_row, building_column])))
                    prk_history.append(prk_score)

    return prk_score, prk_history


def dfs(visited, graph, node):  # function for dfs
    if node not in visited:
        visited.append(node)
        global_visited.append(node)
        for neighbour in get_adjacent_buildings_and_position(node[0], node[1], graph):
            if neighbour[0] == "PRK":
                dfs(visited, graph, [neighbour[1], neighbour[2]])

    return len(visited)


def calculate_mon_score(buildings_tracker):
    mon_score = 0
    mon_history = []
    mon_corner = 0
    corner_score_system = 2
    inside_score_system = 1
    cords = get_corner_coordinates(buildings_tracker)

    for i in cords:
        if buildings_tracker[i[0]][i[1]] == "MON":
            mon_corner = mon_corner + 1

    if mon_corner > 2:
        corner_score_system = 4
        inside_score_system = 4

    for building_row in range(0, len(buildings_tracker)):
        for building_column in range(0, len(buildings_tracker[building_row])):
            build = buildings_tracker[building_row][building_column]
            if build == "MON":
                if [building_row, building_column] in cords:
                    mon_score = mon_score + corner_score_system
                    mon_history.append(corner_score_system)

                else:
                    mon_score = mon_score + inside_score_system
                    mon_history.append(inside_score_system)
    return mon_score, mon_history


def get_corner_coordinates(buildings_tracker):
    cords = []
    cords.append([0, 0])
    cords.append([0, len(buildings_tracker[0]) - 1])
    cords.append([len(buildings_tracker[0]) - 1, 0])
    cords.append([len(buildings_tracker[0]) - 1, len(buildings_tracker[0]) - 1])
    return cords


def get_adjacent_buildings(building_row, pos, buildings_tracker):
    building = []
    # get up
    if building_row > 0:
        building.append(buildings_tracker[building_row - 1][pos])

    # get down
    if building_row < len(buildings_tracker) - 1:
        building.append(buildings_tracker[building_row + 1][pos])

    # get right
    if pos < len(buildings_tracker[building_row]) - 1:
        building.append(buildings_tracker[building_row][pos + 1])

    # get left
    if pos > 0:
        building.append(buildings_tracker[building_row][pos - 1])

    return building


def get_adjacent_buildings_and_position(building_row, pos, buildings_tracker):
    building = []
    # get up
    if building_row > 0:
        building.append([buildings_tracker[building_row - 1][pos], building_row - 1, pos])

    # get down
    if building_row < len(buildings_tracker) - 1:
        building.append([buildings_tracker[building_row + 1][pos], building_row + 1, pos])

    # get right
    if pos < len(buildings_tracker[building_row]) - 1:
        building.append([buildings_tracker[building_row][pos + 1], building_row, pos + 1])

    # get left
    if pos > 0:
        building.append([buildings_tracker[building_row][pos - 1], building_row, pos - 1])

    return building


def see_current_score(buildings_tracker):
    bch_score, bch_score_all = calculate_bch_score(buildings_tracker)
    fac_score, fac_score_all = calculate_fac_score(buildings_tracker)
    hse_score, hse_score_all = calculate_hse_score(buildings_tracker)
    hwy_score, hwy_score_all = calculate_hwy_score(buildings_tracker)
    shp_score, shp_score_all = calculate_shp_score(buildings_tracker)
    prk_score, prk_score_all = calculate_prk_score(buildings_tracker)
    mon_score, mon_score_all = calculate_mon_score(buildings_tracker)

    print("BCH : ", end="")
    print_score_all(bch_score_all)
    print("= " + str(bch_score))

    print("FAC : ", end="")
    print_score_all(fac_score_all)
    print("= " + str(fac_score))

    print("HSE : ", end="")
    print_score_all(hse_score_all)
    print("= " + str(hse_score))

    print("SHP : ", end="")
    print_score_all(shp_score_all)
    print("= " + str(shp_score))

    print("HWY : ", end="")
    print_score_all(hwy_score_all)
    print("= " + str(hwy_score))

    print("PRK : ", end="")
    print_score_all(prk_score_all)
    print("= " + str(prk_score))

    print("MON : ", end="")
    print_score_all(mon_score_all)
    print("= " + str(mon_score))

    TLScore = bch_score + fac_score + hse_score + \
        shp_score + hwy_score + prk_score + mon_score
    print("Total Score = ", TLScore)

    return {"proceed_next_turn": False}


def print_score_all(score_all):
    if (len(score_all) == 0):
        print("0", end=" ")

    for i in range(len(score_all)):
        print(score_all[i], end=" ")
        if(i != len(score_all) - 1):
            print("+", end=" ")


def save_game(board_tracker, buildings_tracker, current_turn, board_metadata):
    game_data = {"board_tracker": board_tracker, "buildings_tracker": buildings_tracker, "current_turn": current_turn, "board_metadata": board_metadata}

    save_data_file = open("save_data.txt", "w")
    save_data_file.write(str(game_data))
    save_data_file.close()

    print("\nGame saved!")
    return {"proceed_next_turn": False}


def load_saved_game():
    print("load saved game")
    return {}


def choose_building_pool():
    while True:
        print("\nCurrent building pool")
        print(building_pool)
        print("1. Change building pool")
        print('0. Exit')

        user_input = input("Your choice? ")
        if user_input == "0":
            return {}
        elif user_input == "1":
            buildings = ["BCH", "FAC", "HSE", "SHP", "HWY", "PRK", "MON"]
            print("\n", buildings)

            user_pool_input = input("Choose 5 different buildings (sep with space): ")
            new_pool = user_pool_input.split(" ")

            pool_valid = validate_building_pool_selection(buildings, new_pool)

            if pool_valid:
                print("Building pool changed successfully")
                return {"bp": new_pool}
        else:
            print("Invalid option, try again")


def validate_building_pool_selection(buildings, new_pool):
    for b in new_pool:
        if b not in buildings:
            print("Invalid building entered, try again")
            return False

    if len(new_pool) != len(set(new_pool)):
        print("Duplicate building entered, try again")
        return False

    if len(new_pool) != 5:
        print("Please enter exactly 5 buildings, try again")
        return False

    return True


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

    sys.exit()


if __name__ == "__main__":
    master_loop()
