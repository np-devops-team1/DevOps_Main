# The Simp Game

# Buildings
# ---------------------- #
# Beach (BCH) , Factory (FAC) , House (HSE) , Shop (SHP) , Highway (HWY)

# Board
# ---------------------- #
# [['A1','B1','C1','D1'],
#  ['A2','B2','C2','D2'],
#  ['A3','B3','C3','D3'],
#  ['A4','B4','C4','D4']]

# Game Options
# -----------------------#
# 6 Options
# 1. Place Random Building
# 2. Place Random Building
# 3. See remaining buildings
# 4. See current score

# 5. Save game
# 0. Exit to main menu

# Imports
import random

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
buildCount = {"BCH": 8, "FAC": 8, "HSE": 8, "SHP": 8, "HWY": 8}
lastPlace = ""  # stores last plot built upon


# module reduces the amount of buildings available after use
def SubtractBuildingCount(number):
    global buildCount
    building = buildings[number]
    buildCount[building] = buildCount[building] - 1


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


# function for main menu
def ControlFlow():
    while True:
        MainGame()


def MainGame():
    FirstMenu()

    try:
        option = (int)(input("Your choice? "))
    except ValueError:
        option = 100

    if option == 1:
        StartGameFunc()
    elif option == 2:
        LoadGameFunc()
    elif option == 0:
        exit(0)
    else:
        print("invalid option, try again")


# generates random option for buildings to be placed on plots
def randomOptionsFunc():
    while True:
        numberOne = random.randint(0, 4)
        if buildCount[buildings[numberOne]] != 0:
            return numberOne


# module returns a list of adjacent locations to the function parameter
def CheckAdjacency(loc):
    if(loc in locationDic.keys()):
        return locationDic.get(loc)
    else:
        raise ValueError('Unexpected location')


def FirstMenu():
    print("Welcome, mayor of Simp City!")
    print("------------------------------")
    print("1. Start new game")
    print("2. Load saved game")
    print("0. Exit")


def printGameMenuFunc(buildingOne, buildingTwo):
    print("1. Build a", buildings[buildingOne])
    print("2. Build a", buildings[buildingTwo])
    print("3. See remaining buildings ")
    print("4. See current score ")
    print("5. Save game ")
    print("0. Exit to main menu ")


def printRemainingBuildings():
    print("--- Remaining Buildings ---")
    print("Beach : ", buildCount["BCH"])
    print("Factory : ", buildCount["FAC"])
    print("House : ", buildCount["HSE"])
    print("Shop : ", buildCount["SHP"])
    print("Highway : ", buildCount["HWY"])


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
    SubtractBuildingCount(option)
    plots["lastPlace"] = position
    plots["Turn"] = (int)(plots["Turn"]) + 1
    CityMapFunc()
    return plots


def SaveGameFunc():
    print("save game")


def ScoreAdjacentBuildings():
    print("score")


def StartGameFunc():
    global plots
    plots["Turn"] = (int)(plots["Turn"]) + 1

    # When turn is not 16
    while (int)(plots["Turn"]) <= 16:
        print("Turn: ", plots["Turn"])
        CityMapFunc()
        optionOne = randomOptionsFunc()
        optionTwo = randomOptionsFunc()
        printGameMenuFunc(optionOne, optionTwo)

        choice = (int)(input("Your choice?"))

        if choice == 1:
            result = buildBuilding(optionOne, plots)

        elif choice == 2:
            result = buildBuilding(optionOne, plots)

        elif choice == 3:
            printRemainingBuildings()
        elif choice == 4:
            print("----------------------------------")
            ScoreAdjacentBuildings(plots)
            continue
        elif choice == 5:
            SaveGameFunc()
            FirstMenu()
            break
        elif choice == 0:
            FirstMenu()
            break

        if result is False:
            continue

        plots = result
    print("----------------------------------")
    ScoreAdjacentBuildings(plots)


def LoadGameFunc():
    print("load")


def __init__():
    ControlFlow()
