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
        self.keylist = None
        self.platformTilesList = None
        self.dangerList = None
        self.myMap = None       
        self.view_bottom = 0
        self.view_left = 0
        self.BackgroundTiles = None
        self.ForegroundTiles = None
        self.playerSprite = None
        self.physics_engine = None
        self.waterList = None
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")

        self.coinsCollectedCounter = 0 

#Custom methods
    #Setups for each object        
    def setupPlayer(self):
        self.playerSprite = CharacterClass(256,256)
    def setupPlatformLayer(self):
        self.platformTilesList = arcade.tilemap.process_layer(map_object=self.myMap,layer_name="Platform",scaling=Const.TILE_SCALE,use_spatial_hash=True)
        if self.myMap.background_color:
            arcade.set_background_color(self.myMap.background_color)
        for tile in arcade.tilemap.process_layer(map_object=self.myMap,layer_name="Platform_Moving",scaling=Const.TILE_SCALE,use_spatial_hash=True):
            self.platformTilesList.append(tile)
    def setupObjects(self):
        #for coordinate in Const.coordinate_list:
            #wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", Const.TILE_SCALE)
            #wall.position = coordinate
            #self.platformTilesList.append(wall)
            pass
    def setupCoins(self):
        self.coinList = arcade.tilemap.process_layer(map_object=self.myMap, layer_name="Coins",scaling=Const.COIN_SCALE,use_spatial_hash=True)
    def setupKeys(self):
        self.keylist = arcade.tilemap._process_tile_layer(map_object=self.myMap, layer="Keys",scaling=Const.COIN_SCALE,use_spatial_hash=True)
    def setupDanger(self):
        self.dangerList = arcade.tilemap.process_layer(map_object=self.myMap, layer_name="Danger",scaling=Const.TILE_SCALE,use_spatial_hash=True)
    def setupDoorsLayer(self):
        pass
    def setupEnemiesLayer(self):
        pass
    def setupForegroundLayer(self):
        self.ForegroundTiles = arcade.tilemap.process_layer(map_object=self.myMap, layer_name="Foreground",scaling=Const.TILE_SCALE,use_spatial_hash=True)
        self.BackgroundTiles = arcade.tilemap.process_layer(map_object=self.myMap, layer_name="Background",scaling=Const.TILE_SCALE,use_spatial_hash=True)
    def setupEngine(self):
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.playerSprite,self.platformTilesList,Const.GRAVITY) #Has to be last method  called of all setups
    def setupWater(self):
        self.waterList = arcade.tilemap.process_layer(map_object=self.myMap, layer_name="Water_Moving_Bgd",scaling=Const.TILE_SCALE,use_spatial_hash=True)
        for tile in arcade.tilemap.process_layer(map_object=self.myMap, layer_name="Water_Moving_Fgd",scaling=Const.TILE_SCALE,use_spatial_hash=True):
            self.waterList.append(tile)
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

    #Checking for collision or moving objects  
    def checkForMovingPlatforms(self):
        for tile in self.platformTilesList:
            if tile.boundary_right and tile.right > tile.boundary_right and tile.change_x > 0:
                tile.change_x *= -1
            if tile.boundary_left and tile.left < tile.boundary_left and tile.change_x < 0:
                tile.change_x *= -1
            if tile.boundary_top and tile.top > tile.boundary_top and tile.change_y > 0:
                tile.change_y *= -1
            if tile.boundary_bottom and tile.bottom < tile.boundary_bottom and tile.change_y < 0:
                tile.change_y *= -1
    def checkForMovingWater(self):
        if self.waterList[0].center_x < -96 or self.waterList[0].center_x > 128:
            for tile in self.waterList:
                tile.change_x *=-1
    def checkForCoinCollision(self):
        coin_hit_list = arcade.check_for_collision_with_list(self.playerSprite, self.coinList)
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)
            self.coinsCollectedCounter += 1
    def checkForDangerCollision(self):
        danger_hit_list = arcade.check_for_collision_with_list(self.playerSprite, self.dangerList)
        if danger_hit_list.__len__() > 0: 
            self.setup("maps/Map2.tmx")
    
    #For moving water bidirectional
    def drawWater(self,isBackorFore):
        waterListLenght = len(self.waterList)
        for i in range(int(waterListLenght/2)):
            it =i
            if (isBackorFore):
                it += waterListLenght/2
            self.waterList[int(it)].draw()

#Arcade build-in methods
    def setup(self,mapName):
        mapName = mapName
        self.myMap = arcade.tilemap.read_tmx(mapName)
        self.setupPlayer()
        self.setupPlatformLayer()
        self.setupObjects()
        self.setupCoins()
        self.setupDanger()
        self.setupForegroundLayer()
        self.setupWater()
        self.setupEngine()
        self.coinsCollectedCounter = 0

    #Order of drawing is important! - Note: best use as leayer in map project
    def on_draw(self):
        arcade.start_render()
        self.BackgroundTiles.draw()
        self.drawWater(False)
        self.dangerList.draw()
        self.playerSprite.draw()
        self.platformTilesList.draw()
        self.coinList.draw()        
        #self.Dors
        #self.keylist().draw()
        self.drawWater(True)
        self.ForegroundTiles.draw()
        score_text = f"Money: {self.coinsCollectedCounter}"
        arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom,
                         arcade.csscolor.WHITE, 18)
    #Character movement
    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.playerSprite.change_y = Const.JUMP_HEIGHT
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.playerSprite.change_x = -Const.MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.playerSprite.change_x = Const.MOVEMENT_SPEED
        elif key == arcade.key.R:
            self.setup("maps/Map2.tmx")
            
    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.playerSprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.playerSprite.change_x = 0

    def on_update(self, delta_time):
        self.physics_engine.update()
        self.playerSprite.update_animation()
        self.platformTilesList.update()
        self.waterList.update()
        self.checkForMovingPlatforms()
        self.screenScroll()
        self.checkForCoinCollision()
        self.checkForDangerCollision()
        self.checkForMovingWater()

        #To discuss self.checkForEnemyCollision()











def main():
    window = GameLauncher()
    window.setup("maps/Map2.tmx")
    arcade.run()

if __name__ == "__main__":
    main()