
import arcade
import constants as Const
from GameObjects.CharacterClass import CharacterClass

class MapClass():
    def __init__(self,mapProps):
        self.baseMap = arcade.tilemap.read_tmx(mapProps[0])
        arcade.set_background_color(Const.BACKGROUND)
        self.kill_enemy_sound = arcade.load_sound(':resources:sounds/hit2.wav') # Think to pass this value in better way
        self.mapProps = mapProps
        self.coinList = None
        self.platformTilesList = None
        self.dangerList = None
        self.enemyList = None
        self.BackgroundTiles = None
        self.ForegroundTiles = None
        self.playerSprite = None
        self.waterList = None
        self.boxList = None
        self.view_bottom = 0
        self.view_left = 0
        self.coinsCollectedCounter = 0 
        self.Exit = None
        self.winText = None
        self.enemies_positions = []
        self.bullet_list = None
    #Map setups for diffrent sprites
    def setupPlayer(self):
        self.playerSprite = CharacterClass(self.mapProps[1],self.mapProps[2])
    def setupPlatformLayer(self):
        self.platformTilesList = arcade.tilemap.process_layer(map_object=self.baseMap,layer_name="Platform",scaling=Const.TILE_SCALE,use_spatial_hash=True)
        if self.baseMap.background_color:
            arcade.set_background_color(self.baseMap.background_color)
        for tile in arcade.tilemap.process_layer(map_object=self.baseMap,layer_name="Platform_Moving",scaling=Const.TILE_SCALE,use_spatial_hash=True):
            self.platformTilesList.append(tile)
    def setupCoins(self):
        self.coinList = arcade.tilemap.process_layer(map_object=self.baseMap, layer_name="Coins",scaling=Const.COIN_SCALE,use_spatial_hash=True)
    def setupDanger(self):
        self.dangerList = arcade.tilemap.process_layer(map_object=self.baseMap, layer_name="Danger",scaling=Const.TILE_SCALE,use_spatial_hash=True)
    def setupForegroundLayer(self):
        self.ForegroundTiles = arcade.tilemap.process_layer(map_object=self.baseMap, layer_name="Foreground",scaling=Const.TILE_SCALE,use_spatial_hash=True)
        self.BackgroundTiles = arcade.tilemap.process_layer(map_object=self.baseMap, layer_name="Background",scaling=Const.TILE_SCALE,use_spatial_hash=True)
    def setupWater(self):
        self.waterList = arcade.tilemap.process_layer(map_object=self.baseMap, layer_name="Water_Moving_Bgd",scaling=Const.TILE_SCALE,use_spatial_hash=True)
        for tile in arcade.tilemap.process_layer(map_object=self.baseMap, layer_name="Water_Moving_Fgd",scaling=Const.TILE_SCALE,use_spatial_hash=True):
            self.waterList.append(tile)
    def setupExit(self):
        self.Exit = arcade.tilemap.process_layer(map_object=self.baseMap, layer_name="EXIT",scaling=Const.TILE_SCALE,use_spatial_hash=True)
    def setupEnemies(self):
        self.enemyList = arcade.tilemap.process_layer(map_object=self.baseMap, layer_name="Enemies",scaling=Const.TILE_SCALE,use_spatial_hash=True)
        for enemy in self.enemyList:
            self.enemies_positions.append([enemy.center_x, True])
    def setupBoxes(self):
        self.boxList = arcade.tilemap.process_layer(map_object=self.baseMap, layer_name="Boxes",scaling=Const.TILE_SCALE,use_spatial_hash=True)
    def setupBullets(self):
        self.bullet_list = arcade.SpriteList()
    #Main setup method to run sub-setups
    def setup(self):
        self.setupPlayer()
        self.setupPlatformLayer()
        self.setupCoins()
        self.setupDanger()
        self.setupForegroundLayer()
        self.setupWater()
        self.setupExit()
        self.setupEnemies()
        self.setupBoxes()
        self.setupBullets()
        self.coinsCollectedCounter = 0
    
    
    def drawWater(self,isBackorFore):
        waterListLenght = len(self.waterList)
        for i in range(int(waterListLenght/2)):
            it =i
            if (isBackorFore):
                it += waterListLenght/2
            self.waterList[int(it)].draw()
    def drawMap(self):
        self.BackgroundTiles.draw()
        self.drawWater(False)
        self.enemyList.draw()   
        self.dangerList.draw()
        self.playerSprite.draw()
        self.platformTilesList.draw()
        self.coinList.draw()     
        self.Exit.draw()
        self.drawWater(True)
        self.boxList.draw()
        self.ForegroundTiles.draw()
        self.DrawText()
    def DrawText(self):
        score_text = f"Money: {self.coinsCollectedCounter}"
        score_remain_text = f"Still to collect: {len(self.coinList)}"
        arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom,
                         arcade.csscolor.WHITE, 18)
        arcade.draw_text(score_remain_text, 10 + self.view_left, 28 + self.view_bottom,
                         arcade.csscolor.WHITE, 18)
    def DrawWinText(self):
        winnerText = f"Wygrales!"
        self.winText =arcade.draw_text(winnerText, self.view_left + Const.SCREEN_WIDTH/2, self.view_bottom + Const.SCREEN_HEIGHT/2  ,arcade.csscolor.WHITE, 36)
    
    def animateEnemies(self):
        enemyIndex = 0
        for enemy in self.enemyList:
            starting_position = self.enemies_positions[enemyIndex][0]
            movingLeft = self.enemies_positions[enemyIndex][1]
            if enemy.center_x >= starting_position - 100 and movingLeft:
                enemy.set_position(enemy.center_x - 2, enemy.center_y)
            else:
                self.enemies_positions[enemyIndex] = [starting_position, False]
                enemy.set_position(enemy.center_x + 2, enemy.center_y)
                if enemy.center_x == starting_position + 100:
                    self.enemies_positions[enemyIndex] = [starting_position, True]
            enemyIndex += 1
    def bulletAnimation(self):
        self.bullet_list.update()
        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemyList)
            box_hit_list = arcade.check_for_collision_with_list(bullet, self.boxList)
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()
            for enemy in hit_list:
                enemy.remove_from_sprite_lists()
                arcade.play_sound(self.kill_enemy_sound)
            for box in box_hit_list:
                box.remove_from_sprite_lists()
    
    def update(self):
        self.playerSprite.update_animation()
        self.platformTilesList.update()
        self.boxList.update()
        self.waterList.update()
        self.animateEnemies()
        self.bulletAnimation()
