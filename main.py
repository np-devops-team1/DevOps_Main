
import random
import ast

# for mapping locations to buildings
plots = {"A1": "\t", "A2": "\t", "A3": "\t", "A4": "\t", "B1": "\t",
         "B2": "\t", "B3": "\t", "B4": "\t", "C1": "\t", "C2": "\t",
         "C3": "\t", "C4": "\t", "D1": "\t", "D2": "\t", "D3": "\t",
         "D4": "\t", "Turn": "0", "lastPlace": ""}

locationDic = {"A1": ["A2", "B1"],
               "A2": ["A1", "A3", "B2"],
               "A3": ["A2", "A4", "B3"],
               "A4": ["A3", "B4"],
               "B1": ["A1", "B2", "C1"],
               "B2": ["A2", "B1", "B3", "C2"],
               "B3": ["A3", "B2", "B4", "C3"],
               "B4": ["A4", "B3", "C4"],
               "C1": ["B1", "C2", "D1"],
               "C2": ["B2", "C1", "C3", "D2"],
               "C3": ["B3", "C2", "C4", "D3"],
               "C4": ["B4", "C3", "D4"],
               "D1": ["C1", "D2"],
               "D2": ["C2", "D1", "D3"],
               "D3": ["D2", "D4", "C3"],
               "D4": ["D3", "C4"]}
buildings = {0: "BCH", 1: "FAC", 2: "HSE", 3: "SHP", 4: "HWY"}
hseScoreDic = {"FAC": 1, "BCH": 2, "HSE": 1, "SHP": 1}
houseHis = []
beachHis = []
factoryScoreHis = []
shopScoreHis = []
highwayScoreHis = []

buildCount = {"BCH": 8, "FAC": 8, "HSE": 8, "SHP": 8, "HWY": 8}
lastPlace = ""  # stores last plot built upon


# module displays game/city grid
def CityMapFunc():
    print("\t     A \t     B \t     C \t     D")
    for i in range(4):
        print("\t   +------------------------------+")
        if i == 0:
            print("\t", i + 1, "| ", plots["A1"], " | ", plots["B1"],
                  " | ", plots["C1"], " | ", plots["D1"], " | ")
        if i == 1:
            print("\t", i + 1, "| ", plots["A2"], " | ", plots["B2"],
                  " | ", plots["C2"], " | ", plots["D2"], " | ")
        if i == 2:
            print("\t", i + 1, "| ", plots["A3"], " | ", plots["B3"],
                  " | ", plots["C3"], " | ", plots["D3"], " | ")
        if i == 3:
            print("\t", i + 1, "| ", plots["A4"], " | ", plots["B4"],
                  " | ", plots["C4"], " | ", plots["D4"], " | ")

    print("\t   +------------------------------+")


def buildBuilding(option, plots):

    position = input("Build where?")

    if position not in plots.keys():
        print("Invalid Position\n")
        return False

    if plots[position] != "\t":
        print("Plot is occupied\n")
        return False

    if (int)(plots["Turn"]) != 0:
        placeList = CheckAdjacency(plots["lastPlace"])
        if position not in placeList:
            print("You must build next to an existing building.")
            return False

    plots[position] = buildings[option]
    # SubtractBuildingCount(option)
    plots["lastPlace"] = position
    plots["Turn"] = (int)(plots["Turn"]) + 1
    CityMapFunc()
    return plots


# module returns a list of adjacent locations to the function parameter
def CheckAdjacency(loc):
    if(loc in locationDic.keys()):
        return locationDic.get(loc)
    else:
        raise ValueError('Unexpected location')


# Functions to calculate scores
# calculate BCH score
def calculateBCHscore(place):
    placeSplit = list(place)
    row = placeSplit[0]
    # col = placeSplit[1]
    rowLeft = list(plots.keys())[0][0]
    rowRight = list(plots.keys())[-3][0]

    if (row == rowLeft or row == rowRight):
        return 3
    else:
        return 1


# calculate factory score
def calculateFACscore(factoryNumber):

    if (isinstance(factoryNumber, int)):
        if factoryNumber < 5:
            factoryScoreHis = [factoryNumber for i in range(factoryNumber)]
            return factoryNumber * factoryNumber
        else:
            factoryNumber = factoryNumber - 4
            factoryScoreHis = [4 for i in range(4)]
            factoryScoreHis.append([1 for i in range(factoryNumber)])
            return factoryNumber
    else:
        raise TypeError('Invalid Data Type')


def calculateSHPscore(adjacencylist, plots):
    fcount = 0
    bcount = 0
    scount = 0
    hcount = 0
    shopScore = 0

    for item in adjacencylist:
        if plots[item] == "FAC":
            if fcount == 1:
                break
            shopScore = shopScore + 1
            fcount = fcount + 1
        elif plots[item] == "BCH":
            if bcount == 1:
                break
            shopScore = shopScore + 2
            bcount = bcount + 1
        elif plots[item] == "HSE":
            if hcount == 1:
                break
            shopScore = shopScore + 1
            hcount = hcount + 1
        elif plots[item] == "SHP":
            if scount == 1:
                break
            shopScore = shopScore + 1
            scount = scount + 1
    return shopScore


def calculateHSEscore(plots, item):
    if (plots[item] in hseScoreDic.keys()):
        return hseScoreDic.get(plots[item])
    else:
        return 0


def calculateHWYscore(adjacencylist, plots):
    for item in adjacencylist:
        if plots[item] == "HWY":
            return 1
            print("Highway Score + 1")
    return 0


def printScoreHis(history):
    for i in range(len(history)):
        print(history[i], end=" ")
        if(i != len(history)):
            print("+", end=" ")


# function incorportes scoring logic for all types of buildings
def ScoreAdjacentBuildings(plots):
    TLScore, houseScore, beachScore, factoryScore, shopScore, highwayScore = 0
    global houseHis, beachHis, factoryScoreHis, shopScoreHis, highwayScoreHis

    factoryNumber = 0

    for place, build in plots.items():
        if build == "BCH":
            score = calculateBCHscore(place)
            beachScore = beachScore + score
            beachHis.append(score)

        if build == "FAC":
            factoryNumber = factoryNumber + 1
        if build == "HSE":
            adjacencylist = CheckAdjacency(place)
            for item in adjacencylist:
                score = calculateHSEscore(plots, item)
                houseScore = houseScore + score
                houseHis.append(score)

        if build == "SHP":
            adjacencylist = CheckAdjacency(place)
            score = calculateSHPscore(adjacencylist, plots)
            shopScore = shopScore + score
            shopScoreHis.append(score)
        if build == "HWY":
            adjacencylist = CheckAdjacency(place)
            score = calculateHWYscore(adjacencylist, plots)
            highwayScore = highwayScore + score
            highwayScoreHis.append(score)

    factoryScore = calculateFACscore(factoryNumber)

    print("BCH : ", printScoreHis(beachHis) + " = " + beachScore)
    print("FAC : ", printScoreHis(factoryScoreHis) + " = " + factoryScore)
    print("HSE : ", printScoreHis(houseHis) + " = " + houseScore)
    print("SHP : ", printScoreHis(shopScoreHis) + " = " + shopScore)
    print("HWY : ", printScoreHis(highwayScoreHis) + " = " + highwayScore)

    TLScore = beachScore + factoryScore + houseScore + shopScore + highwayScore
    print("Total Score = ", TLScore)


# module saves game data to txt file
def save_game():
    return False


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
    return


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
    print(" ", buildings_tracker)

    for row_index, row_value in enumerate(board_tracker, start=1):
        print(row_divider)
        print(" {}|".format(row_index), end="")
        for cell in row_value:
            if cell == "":
                print("     |", end="")
            else:
                print(" " + cell + " |", end="")
        print()
    print(row_divider)


def build_building():
    return False


def see_current_score():
    return False


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


def load_saved_game():
    try:
        with open("dict.txt") as f:
            data = f.read()
        loadedPlots = ast.literal_eval(data)
        print(plots)

        with open("buildingCount.txt") as file:
            dataBuild = file.read()
        loadedBuildings = ast.literal_eval(dataBuild)
        return loadedPlots, loadedBuildings, True
    except FileNotFoundError:
        print("File is not found")
        return plots, buildCount, False
    except ValueError:
        print("Loaded Data is incorrect")
        return plots, buildCount, False
    except SyntaxError:
        print("Loaded Data is incorrect")
        return plots, buildCount, False


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
