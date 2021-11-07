#The Simp Game

# Buildings
#----------------------#
# Beach (BCH) , Factory (FAC) , House (HSE) , Shop (SHP) , Highway (HWY)

#Board
#----------------------#
# [['A1','B1','C1','D1'],
#  ['A2','B2','C2','D2'],
#  ['A3','B3','C3','D3'],
#  ['A4','B4','C4','D4']]

#Game Options
#-----------------------#
# 6 Options
# 1. Place Random Building
# 2. Place Random Building
# 3. See remaining buildings
# 4. See current score

# 5. Save game
# 0. Exit to main menu

#Imports
import random

#Main Menu
#----------------------#
def displayMainMenu():
    #optionsMain = ['1. Start new game','2. Load saved game','0. Exit']
    print('Welcome, mayor of Simp City!')
    print('----------------------------')
    print('1. Start new game')
    print('2. Load saved game')
    print('0. Exit')
    print('Your choice?')

def displayGameMenu(random1,random2):
    buildings = ['BCH' , 'FAC' , 'HSE' , 'SHP' , 'HWY']
    print(f'1. Build a {buildings[random1]}')
    print(f'2. Build a {buildings[random2]}')
    print(f'3. See remaining buildings')
    print(f'4. See current score')
    print()
    print(f'5. Save game')
    print(f'0. Exit to main menu')


def startGame():
    #Initialize
    buildingsRemaining = [8,8,8,8,8]
    board = [['     ','     ','     ','     '],
    ['     ','     ','     ','     '],
    ['     ','     ','     ','     '],
    ['     ','     ','     ','     ']]
    score = 0
    turns = 0
    gameRunning = True
    while gameRunning:
        #Current Board
        print(f'Turn {turns}')
        print(f'    A     B     C     D   ')
        print(f' +-----+-----+-----+-----+')
        print(f'1|{board[0][0]}|{board[0][1]}|{board[0][2]}|{board[0][3]}|')
        print(f' +-----+-----+-----+-----+')
        print(f'1|{board[1][0]}|{board[1][1]}|{board[1][2]}|{board[1][3]}|')
        print(f' +-----+-----+-----+-----+')
        print(f'1|{board[2][0]}|{board[2][1]}|{board[2][2]}|{board[2][3]}|')
        print(f' +-----+-----+-----+-----+')
        print(f'1|{board[3][0]}|{board[3][1]}|{board[3][2]}|{board[3][3]}|')
        print(f' +-----+-----+-----+-----+')

        randomBuilding1 = random.randint(1,5)
        randomBuilding2 = random.randint(1,5)
        displayGameMenu()
        playerOption = input('Your Choice? ')
        if playerOption == '1':
            #Build1
            print('Build1')
        elif playerOption == '2':
            #Build2
            print('Build1')
        elif playerOption == '3':
            #See Remaining buildings
            print('Remaining buildings')
        elif playerOption == '4':
            #See currentScore
            print('Current Score')
        elif playerOption == '5':
            #Save Game
            print('Save')
        elif playerOption == '0':
            #Exit to main menu
            print('Exit')
        else:
            print('What the hell did you just put?')
            continue


