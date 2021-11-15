# mainMenuTest.py

import pytest
from main import Game

def test_mainMenu():
    assert Game.displayMainMenu() == None