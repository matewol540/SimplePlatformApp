"""
Platform game created by Mateusz Wolski & Dawid Krakowczyk
"""

import arcade
import constants as Const
import json
from CharacterClass import CharacterClass

class GameLauncher(arcade.Window):
    def __init__(self):
        super().__init__(Const.SCREEN_WIDTH, Const.SCREEN_HEIGHT, Const.APP_TITLE)
        arcade.set_background_color(Const.BACKGROUND)
        self.coinList = None
        self.wallList = None
        self.playerList = None
        self.ladderList = None #To be added
        
        self.view_bottom = 0
        self.view_left = 0

        self.playerSprite = None
        self.physics_engine = None

        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")


#Custom methods
    #Setups for each object        
    def setupPlayer(self):
        self.playerList = arcade.SpriteList()
        self.playerSprite = CharacterClass()
        self.playerSprite.center_x = 64
        self.playerSprite.center_y = 128
        self.playerList.append(self.playerSprite)
    def setupMap(self):
        for x in range(0, 1250, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", Const.TILE_SCALE)
            wall.center_x = x
            wall.center_y = 32
            self.wallList.append(wall)
    def setupObjects(self):
        for coordinate in Const.coordinate_list:
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", Const.TILE_SCALE)
            wall.position = coordinate
            self.wallList.append(wall)
    def setupEngine(self):
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.playerSprite,self.wallList,Const.GRAVITY) #Has to be last method  called of all setups
    def setupCoins(self):
        self.coinList = arcade.SpriteList(use_spatial_hash=True)
        for coordinate in Const.coordinate_list:
            coin = arcade.Sprite(":resources:images/items/coinGold.png", Const.COIN_SCALE)
            coin.center_x = coordinate[0]
            coin.center_y = 200
            self.coinList.append(coin)

    #Camera scroll
    def screenScroll(self):
        changed = False

        # Scroll left
        left_boundary = self.view_left + Const.LEFT_VIEWPORT_MARGIN
        if self.playerSprite.left < left_boundary:
            self.view_left -= left_boundary - self.playerSprite.left
            changed = True
        # Scroll right
        right_boundary = self.view_left + Const.SCREEN_WIDTH - Const.RIGHT_VIEWPORT_MARGIN
        if self.playerSprite.right > right_boundary:
            self.view_left += self.playerSprite.right - right_boundary
            changed = True
        # Scroll up
        top_boundary = self.view_bottom + Const. SCREEN_HEIGHT - Const.TOP_VIEWPORT_MARGIN
        if self.playerSprite.top > top_boundary:
            self.view_bottom += self.playerSprite.top - top_boundary
            changed = True
        # Scroll down
        bottom_boundary = self.view_bottom + Const.BOTTOM_VIEWPORT_MARGIN
        if self.playerSprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.playerSprite.bottom
            changed = True
        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                Const.SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                Const.SCREEN_HEIGHT + self.view_bottom)

    #Game load
    def LoadSave():
        pass

    #Checking for collision   
    def checkForCoinCollision(self):
        coin_hit_list = arcade.check_for_collision_with_list(self.playerSprite, self.coinList)
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)

#Arcade build-in methods
    def setup(self):
        self.wallList = arcade.SpriteList(use_spatial_hash=True)
        self.setupPlayer()
        self.setupMap()
        self.setupObjects()
        self.setupCoins()

        self.setupEngine()

    def on_draw(self):
        arcade.start_render()
        self.wallList.draw()
        self.playerList.draw()
        self.coinList.draw()        

    #Character movement
    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.playerSprite.change_y = Const.JUMP_HEIGHT
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.playerSprite.change_x = -Const.MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.playerSprite.change_x = Const.MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.playerSprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.playerSprite.change_x = 0

    def on_update(self, delta_time):
        self.physics_engine.update()
        self.screenScroll()
        self.checkForCoinCollision()
        #To discuss self.checkForEnemyCollision()

def main():
    window = GameLauncher()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()