"""
Platform game created by Mateusz Wolski & Dawid Krakowczyk
"""

import arcade

#VIEW PROPS
APP_TITLE = f"Simple game"
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 250
BOTTOM_VIEWPORT_MARGIN = 200
TOP_VIEWPORT_MARGIN = 200

#Character props

RIGHT_FACING = 0
LEFT_FACING = 1
GRAVITY = 0.8
CHARACTER_SCALE = 1

#Game props
BACKGROUND = arcade.csscolor.CORNFLOWER_BLUE
TILE_SCALE = 1  
COIN_SCALE = 1

MapList = [["maps/Map1.tmx",256,256],["maps/Map2.tmx",256,256],["maps/Map3.tmx",256,256]]

#Test objects
coordinate_list = [[512, 96],[256, 96],[768, 96]]