import arcade
import constants as Const
import json
import math
from Views.GameWindow import GameWindow

def main():
    window = GameWindow()
    window.LoadInitialScreen()
    arcade.run()

if __name__ == "__main__":
    main()