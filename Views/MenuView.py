import arcade 
import threading
import constants as Const
from Views.GameView import GameView

class MenuView(arcade.View):

    def __init__(self):
        super().__init__()
        self.textButton= arcade.Sprite()
        self.animationExecCntr = 0
        self.IncreaseAnimationCntr = False 
        self.audio_player = arcade.play_sound(self.window.main_theme)

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Game Launcher", Const.SCREEN_WIDTH/2, Const.SCREEN_HEIGHT/2,
                         arcade.color.BLACK, font_size=60, anchor_x="center")
        self.textButton = arcade.draw_text("Press any key to start", Const.SCREEN_WIDTH/2, Const.SCREEN_HEIGHT/2-220,
                         arcade.color.ORANGE, font_size=20, anchor_x="center")
        arcade.draw_ellipse_filled(self.textButton._get_center_x(), self.textButton._get_center_y(), self.textButton._get_width().__int__() + 80,self.textButton._get_height().__int__() + 60,arcade.color.BLACK )
        self.textButton.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        arcade.stop_sound(self.audio_player)
        
        gameView = GameView()
        gameView.LoadMap(Const.MapList[0])
        self.window.show_view(gameView)

    def on_update(self, delta_time):
        self.animatePlayButton()

    def animatePlayButton(self):
        if self.IncreaseAnimationCntr:
            self.textButton._set_width(self.textButton._get_width() + 0.2)
            self.textButton._set_height(self.textButton._get_height() + 0.2)
        else:
            self.textButton._set_width(self.textButton._get_width() - 0.2)
            self.textButton._set_height(self.textButton._get_height() - 0.2)
        self.animationExecCntr +=1
        if self.animationExecCntr > 75:
            self.animationExecCntr = 0
            self.IncreaseAnimationCntr = not self.IncreaseAnimationCntr 

        
       