import arcade 
import constants as Const
from Views.MenuView import MenuView

#Main class which inherits from arcade.Window/ responsible for displaying proper views 
class GameWindow(arcade.Window):
    #Constructor of GameWindow class
    def __init__(self):
        super().__init__(Const.SCREEN_WIDTH,Const.SCREEN_HEIGHT,Const.APP_TITLE,resizable=False)
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump2.wav")
        self.death_sound = arcade.load_sound(":resources:sounds/gameover1.wav")
        self.main_theme = arcade.load_sound(':resources:music/funkyrobot.mp3')
        self.finish_sound = arcade.load_sound(':resources:sounds/upgrade5.wav')
        self.laser_sound = arcade.load_sound(':resources:sounds/laser1.wav')
    #Method to load initial screen of game
    def LoadInitialScreen(self):   
        MenuObject = MenuView()
        super().show_view(MenuObject)


