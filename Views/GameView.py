import arcade
import math
import constants as Const
from GameObjects.MapClass import MapClass


class GameView(arcade.View):
    def __init__(self): 
        super().__init__()
        self.myMap = None   
        self.physics_engine = None
        self.player = None
        self.audio_player = None

    #Do handlings for game events
    def screenScroll(self):
        changed = False

        # Scroll left
        left_boundary = self.myMap.view_left + Const.LEFT_VIEWPORT_MARGIN
        if self.playerSprite.left < left_boundary:
            self.myMap.view_left -= left_boundary - self.playerSprite.left
            changed = True
        # Scroll right
        right_boundary = self.myMap.view_left + Const.SCREEN_WIDTH - Const.RIGHT_VIEWPORT_MARGIN
        if self.playerSprite.right > right_boundary:
            self.myMap.view_left += self.playerSprite.right - right_boundary
            changed = True
        # Scroll up
        top_boundary = self.myMap.view_bottom + Const. SCREEN_HEIGHT - Const.TOP_VIEWPORT_MARGIN
        if self.playerSprite.top > top_boundary:
            self.myMap.view_bottom += self.playerSprite.top - top_boundary
            changed = True
        # Scroll down
        bottom_boundary = self.myMap.view_bottom + Const.BOTTOM_VIEWPORT_MARGIN
        if self.playerSprite.bottom < bottom_boundary:
            self.myMap.view_bottom -= bottom_boundary - self.playerSprite.bottom
            changed = True
        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.myMap.view_bottom = int(self.myMap.view_bottom)
            self.myMap.view_left = int(self.myMap.view_left)

            # Do the scrolling
            arcade.set_viewport(self.myMap.view_left,
                                Const.SCREEN_WIDTH + self.myMap.view_left,
                                self.myMap.view_bottom,
                                Const.SCREEN_HEIGHT + self.myMap.view_bottom)
    def checkForMovingPlatforms(self):
        for tile in self.myMap.platformTilesList:
            if tile.boundary_right and tile.right > tile.boundary_right and tile.change_x > 0:
                tile.change_x *= -1
            if tile.boundary_left and tile.left < tile.boundary_left and tile.change_x < 0:
                tile.change_x *= -1
            if tile.boundary_top and tile.top > tile.boundary_top and tile.change_y > 0:
                tile.change_y *= -1
            if tile.boundary_bottom and tile.bottom < tile.boundary_bottom and tile.change_y < 0:
                tile.change_y *= -1
    def checkForMovingWater(self):
        if self.myMap.waterList[0].center_x < -96 or self.myMap.waterList[0].center_x > 128:
            for tile in self.myMap.waterList:
                tile.change_x *=-1
    def checkForCoinCollision(self):
        coin_hit_list = arcade.check_for_collision_with_list(self.playerSprite, self.myMap.coinList)
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.window.collect_coin_sound)
            self.myMap.coinsCollectedCounter += 1
    def checkForDangerCollision(self):
        danger_hit_list = arcade.check_for_collision_with_list(self.playerSprite, self.myMap.dangerList)
        if danger_hit_list.__len__() > 0: 
            self.LoadMap(self.myMap.mapProps)
            arcade.play_sound(self.window.death_sound)
    def checkForEnemiesCollision(self):
        enemies_hit_list = arcade.check_for_collision_with_list(self.playerSprite, self.myMap.enemyList)
        if enemies_hit_list.__len__() > 0: 
            self.LoadMap(self.myMap.mapProps)
            arcade.play_sound(self.window.death_sound)
    def checkForExitCollision(self):
        exit_Collision_List = arcade.check_for_collision_with_list(self.playerSprite, self.myMap.Exit)
        if (exit_Collision_List.__len__()> 0):
            self.myMap.DrawWinText()
            arcade.play_sound(self.window.jump_sound)
            if (Const.MapList[0][0] == self.myMap.mapProps[0]):
                self.LoadMap(Const.MapList[1])
            else:
                self.LoadMap(Const.MapList[2])
    def checkForCollisionWithBoxes(self):
        any_collisions = arcade.check_for_collision_with_list(self.playerSprite, self.myMap.boxList)
        if len(any_collisions) > 0:
            self.playerSprite.angle *= -1
            self.playerSprite.change_x = -math.sin(math.radians(self.playerSprite.angle)) * 6
            self.playerSprite.center_x += self.playerSprite.change_x
            self.playerSprite.center_y += self.playerSprite.change_y
    
    def setupEngine(self):
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.myMap.playerSprite,self.myMap.platformTilesList,Const.GRAVITY) #Has to be last method  called of all setups
        if self.audio_player:
            arcade.stop_sound(self.audio_player)
        self.audio_player = arcade.play_sound(self.window.main_theme)

    
    def LoadMap(self,mapName):
        self.myMap = MapClass(mapName)
        self.myMap.setup()
        self.playerSprite = self.myMap.playerSprite
        self.setupEngine()     

    #Arcade build-in methods
    #Order of drawing is important! - Note: best use as leayer in map project
    def on_draw(self):
        arcade.start_render()
        self.myMap.drawMap()
        self.myMap.bullet_list.draw()
    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.playerSprite.change_y = self.playerSprite.CharacterProperties.JUMP_HEIGHT
                arcade.play_sound(self.window.jump_sound)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.playerSprite.change_x = -self.playerSprite.CharacterProperties.MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.playerSprite.change_x = self.playerSprite.CharacterProperties.MOVEMENT_SPEED
        elif key == arcade.key.R:
            self.LoadMap(self.myMap.mapProps)
    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.playerSprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.playerSprite.change_x = 0
    def on_mouse_release(self, x, y,button, modifiers):
        print("released")
    def on_mouse_press(self, x, y, button, modifiers):
        """ Called whenever the mouse button is clicked. """

        bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", 0.7)

        start_x = self.playerSprite.center_x
        start_y = self.playerSprite.center_y
        bullet.center_x = start_x
        bullet.center_y = start_y

        dest_x = x + self.myMap.view_left
        dest_y = y + self.myMap.view_bottom
        
        print(dest_x)
        print(dest_y)

        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        bullet.angle = math.degrees(angle)
        print(f"Bullet angle: {bullet.angle:.2f}")

        bullet.change_x = math.cos(angle) * 20
        bullet.change_y = math.sin(angle) * 20
        arcade.play_sound(self.window.laser_sound)
        self.myMap.bullet_list.append(bullet)

    def on_update(self, delta_time):
        self.physics_engine.update()
        self.myMap.update()
        self.checkForMovingPlatforms()
        self.screenScroll()
        self.checkForCoinCollision()
        self.checkForDangerCollision()
        self.checkForEnemiesCollision()
        self.checkForMovingWater()
        self.checkForCollisionWithBoxes()
        self.checkForExitCollision()

        