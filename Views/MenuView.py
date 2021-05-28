import arcade 
import threading

from arcade.arcade_types import Color
import constants as Const
from Views.GameView import GameView

class MenuView(arcade.View):

    def __init__(self):
        super().__init__()
        self.textButton= arcade.Sprite()
        self.animationExecCntr = 0
        self.title = arcade.Sprite()
        self.IncreaseAnimationCntr = False 
        self.audio_player = arcade.play_sound(self.window.main_theme)
        self.background = arcade.load_texture("Assets/menu-bg.png")
        self.IsLoadingGameExec = False
        

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        if  not self.IsLoadingGameExec:
            arcade.draw_lrwh_rectangle_textured(0, 0, Const.SCREEN_WIDTH, Const.SCREEN_HEIGHT, self.background)
            self.title = arcade.draw_text("Projekt zaliczeniowy", Const.SCREEN_WIDTH/2, Const.SCREEN_HEIGHT/2 + 150,
                             arcade.color.WHITE, font_size=60, anchor_x="center")
            arcade.draw_text("Mateusz Wolski", 112, 80, arcade.color.WHITE, font_size=18, anchor_x="center")
            arcade.draw_text("Dawid Krakowczyk", 128,50, arcade.color.WHITE, font_size=18, anchor_x="center")
            arcade.draw_text("WSB Chorzów - Semestr II - Zaliczenie dr. Lesław Pawlaczyk", 340, 20, arcade.color.WHITE, font_size=18, anchor_x="center")
            self.textButton = arcade.draw_text("Naciśnij dowolny przycisk", Const.SCREEN_WIDTH/2, Const.SCREEN_HEIGHT/2-150,
                             arcade.color.WHITE, font_size=20, anchor_x="center")
            arcade.draw_rectangle_filled(self.textButton._get_center_x(), self.textButton._get_center_y(), self.textButton._get_width().__int__() + 80,self.textButton._get_height().__int__() + 60, arcade.color.BLACK )
            self.textButton.draw()
        if self.IsLoadingGameExec:
            self.DisplayLoadingScreenPlaceholder()

        arcade.finish_render()


    def on_key_press(self, symbol: int, modifiers: int):
        arcade.stop_sound(self.audio_player)
        self.IsLoadingGameExec = True
        

    def on_update(self, delta_time):
        if  not self.IsLoadingGameExec:
            self.animatePlayButton()
        

    def animatePlayButton(self):
        if self.IncreaseAnimationCntr:
            self.textButton._set_width(self.textButton._get_width() + 0.1)
        else:
            self.textButton._set_width(self.textButton._get_width() - 0.1)
        self.animationExecCntr += .5
        if self.animationExecCntr > 75:
            self.animationExecCntr = 0
            self.IncreaseAnimationCntr = not self.IncreaseAnimationCntr 

    def DisplayLoadingScreenPlaceholder(self):
        for i in range(200):
            arcade.start_render()
            arcade.draw_rectangle_filled(Const.SCREEN_WIDTH/2, Const.SCREEN_HEIGHT/2, 200 + i*10, 200 +i*10, arcade.color.BLACK)
        arcade.draw_text("LOADING ...",Const.SCREEN_WIDTH/2,Const.SCREEN_HEIGHT/2,arcade.color.WHITE,50,anchor_x="center")
        arcade.finish_render()
        gameView = GameView()
        gameView.LoadMap(Const.MapList[0])
        self.window.show_view(gameView)
       