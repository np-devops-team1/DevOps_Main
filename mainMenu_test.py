# mainMenuTest.py

import pytest
from main import Game

#Ensure that it display main menu

#Ensure that it display game menu
def testFailToDisplayGameMenuIfNoParameters():
    with pytest.raises(ValueError):
        empty = ""
        Game.displayGameMenu(empty, empty)
