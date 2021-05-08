import arcade
import constants as Const


class CharacterClass(arcade.Sprite):
    def __init__(self):
        self.image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        super().__init__(self.image_source,Const.CHARACTER_SCALE)
        
