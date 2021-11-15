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

class Game():
    
    def displayMainMenu():
        #optionsMain = ['1. Start new game','2. Load saved game','0. Exit']
        print('Welcome, mayor of Simp City!')
        print('----------------------------')
        print('1. Start new game')
        print('2. Load saved game')
        print('0. Exit')
        print('Your choice?')

    def displayGameMenu(random1,random2):
        if(random1 in range(1, 6)) and (random2 in range(1, 6)):
            buildings = ['BCH' , 'FAC' , 'HSE' , 'SHP' , 'HWY']
            print(f'1. Build a {buildings[random1]}')
            print(f'2. Build a {buildings[random2]}')
            print(f'3. See remaining buildings')
            print(f'4. See current score')
            print()
            print(f'5. Save game')
            print(f'0. Exit to main menu')
        else:
            raise ValueError("Value Error")
