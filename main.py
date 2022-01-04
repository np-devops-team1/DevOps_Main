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

# function for main menu
def ControlFlow():
    while True:
        MainGame()


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


def FirstMenu():
    print("Welcome, mayor of Simp City!")
    print("------------------------------")
    print("1. Start new game")
    print("2. Load saved game")
    print("0. Exit")


def StartGameFunc():
    print("start")


def LoadGameFunc():
    print("load")
