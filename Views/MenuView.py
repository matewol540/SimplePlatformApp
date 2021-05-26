import arcade 
import constants as Const
from Views.GameView import GameView

class MenuView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Menu Screen", Const.SCREEN_WIDTH/2, Const.SCREEN_HEIGHT/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Press any key to start", Const.SCREEN_WIDTH/2, Const.SCREEN_HEIGHT/2-75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_key_press(self, symbol: int, modifiers: int):
        print("Get signal to start game")
        gameView = GameView()
        gameView.LoadMap(Const.MapList[0])
        self.window.show_view(gameView)
