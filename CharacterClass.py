import arcade
import json
import constants as Const


class CharacterClass(arcade.Sprite):
    class CharacterClassproperties(json.JSONEncoder):
        def default(self):
            return o.__dict__  
        def __init__(self):
            self.VIEW_DISTANCE = 200
            self.MOVEMENT_SPEED = 4
            self.JUMP_HEIGHT = 15
            self.ALL_COINS_COUNTER = 0
            print(self.LoadGameState()) #Zrobic zapis do pliku tego i odczyt 

        def LoadGameState(self):
            return json.dumps(self,default=lambda o:o.__dict__,sort_keys=True,indent=4)

    def __init__(self,center_x,center_y):
        super().__init__()
        self.CharacterProperties = self.CharacterClassproperties()
        self.center_x = center_x
        self.center_y = center_y
        

        self.character_face_direction = Const.RIGHT_FACING
        self.cur_texture = 0
        main_path = ":resources:images/animated_characters/male_person/malePerson"

        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False

        
        self.idle_texture_pair = self.load_texture_pair(f"{main_path}_idle.png")
        self.jump_texture_pair = self.load_texture_pair(f"{main_path}_jump.png")
        self.fall_texture_pair = self.load_texture_pair(f"{main_path}_fall.png")


        self.walk_textures = []
        for i in range(8):
            self.walk_textures.append(self.load_texture_pair(f"{main_path}_walk{i}.png"))

        self.climbing_textures = []
        for i in range(2):
            self.climbing_textures.append(arcade.load_texture(f"{main_path}_climb{i}.png"))

        self.texture = self.idle_texture_pair[0]

        self.set_hit_box(self.texture.hit_box_points)
    

    def load_texture_pair(self,filename):
        return [
            arcade.load_texture(filename),
            arcade.load_texture(filename, flipped_horizontally=True)
        ]
    def update_animation(self, delta_time: float = 1/60):

     # Flipping face direction
        if self.change_x < 0 and self.character_face_direction == Const.RIGHT_FACING:
            self.character_face_direction = Const.LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == Const.LEFT_FACING:
            self.character_face_direction = Const.RIGHT_FACING

     # Climbing animation
        if self.is_on_ladder:
            self.climbing = True
        if not self.is_on_ladder and self.climbing:
            self.climbing = False
        if self.climbing and abs(self.change_y) > 1:
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
        if self.climbing:
            self.texture = self.climbing_textures[self.cur_texture // 4]
            return

     # Jumping animation
        if self.change_y > 0 and not self.is_on_ladder:
            self.texture = self.jump_texture_pair[self.character_face_direction]
            return
        elif self.change_y < 0 and not self.is_on_ladder:
            self.texture = self.fall_texture_pair[self.character_face_direction]
            return

     # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

     # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 7:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]
