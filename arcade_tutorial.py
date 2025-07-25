import arcade
import os
import random
import time

# Constants
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900
WINDOW_TITLE = "Game"

TILE_SCALING = 1
PLAYER_JUMP_SPEED = 5
GRAVITY = 0.5

MOVEMENT_SPEED = 1
UPDATES_PER_FRAME = 5

RIGHT_FACING = 0
LEFT_FACING = 1

CHARACTER_SCALING = 0.5

class MenuView(arcade.View):
    def on_show_view(self):
        self.window.background_color =  arcade.color.COSMIC_LATTE
    
    def on_draw(self):
        self.clear()
        arcade.draw_text("Welcome to Frog Adventures", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, arcade.color.BLACK, font_size = 50, anchor_x="center")
        arcade.draw_text("Click to advance", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 75, arcade.color.GRAY, font_size=25, anchor_x="center")
    
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        instruction_view = InstructionView()
        self.window.show_view(instruction_view)

class InstructionView(arcade.View):
    def on_show_view(self):
        self.window.background_color = arcade.color.GO_GREEN
    
    def on_draw(self):
        self.clear()
        arcade.draw_text("You are a Frog, and must collect all the coins and diamonds, securing them in your chest.", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("WASD / ARROW KEYS to move, Double tap jump to double jump.", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")
        arcade.draw_text("Click to advance", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 85, arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        self.window.show_view(game_view)



class PlayerCharacter(arcade.Sprite):
    def __init__(self, idle_texture_pair, walk_texture_pairs, jump_texture_pair, fall_texture_pair):
        self.character_face_direction = RIGHT_FACING
        self.cur_texture = 0

        self.idle_texture_pair = idle_texture_pair
        self.walk_textures = walk_texture_pairs
        self.jump_texture_pair = jump_texture_pair
        self.fall_texture_pair = fall_texture_pair

        super().__init__(self.idle_texture_pair[0], scale=CHARACTER_SCALING)
        
        self.jump_count = 0
        self.max_jumps = 1
        

    def update_animation(self, delta_time: float = 1 / 60):

        if self.change_x < 0:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0:
            self.character_face_direction = RIGHT_FACING


        if self.change_y > 0:
            self.texture = self.jump_texture_pair[self.character_face_direction]
            return


        if self.change_y < 0:
            self.texture = self.fall_texture_pair[self.character_face_direction]
            return


        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return


        self.cur_texture += 1
        if self.cur_texture >= 8 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        frame = self.cur_texture // UPDATES_PER_FRAME
        direction = self.character_face_direction
        self.texture = self.walk_textures[frame][direction]


class GameView(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

        self.tile_map = None
        self.scene = None
        self.camera = None
        self.gui_camera = None
        self.player_sprite_list = None
        self.physics_engine = None

        self.player = None
        
        self.lives = 3
        self.font_size = 20
        self.font_color = arcade.color.WHITE
        
        self.score = 0
        
        character = "frog_man/frog_man"
    
        idle = arcade.load_texture(f"{character}_idle0.png")
        self.idle_texture_pair = idle, idle.flip_left_right()

        self.walk_texture_pairs = []
        for i in range(8):
            texture = arcade.load_texture(f"{character}_walk{i}.png")
            self.walk_texture_pairs.append((texture, texture.flip_left_right()))

        jump = arcade.load_texture(f"{character}_jump.png")
        self.jump_texture_pair = jump, jump.flip_left_right()

        fall = arcade.load_texture(f"{character}_fall.png")
        self.fall_texture_pair = fall, fall.flip_left_right()

    def setup(self):
        layer_options = {
            "Platform": {
                "use_spatial_hash": True
            },
            "Coins": {
                "use_spatial_hash": True
            },
            "Danger": {
                "use_spatial_hash": True
            },
            "Diamond": {
                "use_spatial_hash": True
            },
            "x_moving_platform": {
                "use_spatial_hash": True
            },
            "y_moving_pla   tform": {
                "use_spatial_hash": True
            },
            "moving_danger": {
                "use_spatial_hash": True
            }
        }

        map_path = os.path.join(os.path.dirname(__file__), "level1.tmx")

        self.tile_map = arcade.load_tilemap(
            map_path,
            scaling=TILE_SCALING,
            layer_options=layer_options,
        )

        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        

        self.player_sprite_list = arcade.SpriteList()
        
        
        self.player = PlayerCharacter(
            self.idle_texture_pair,
            self.walk_texture_pairs,
            self.jump_texture_pair,
            self.fall_texture_pair
        )
        self.player.center_x = 50
        self.player.center_y = 100
        self.spawn_x = self.player.center_x
        self.spawn_y = self.player.center_y
        self.player_sprite_list.append(self.player)
        self.scene.add_sprite("Player", self.player)
        self.scene.add_sprite_list_before("Foreground", "Player")
        
        
        if "x_moving_platform" in self.scene:
            for platform in self.scene["x_moving_platform"]:
                platform.boundary_left = platform.center_x
                platform.boundary_right = platform.center_x + 260
                
        if "y_moving_platform" in self.scene:
            for platform in self.scene["y_moving_platform"]:
                platform.boundary_top = platform.center_y + 370
                platform.boundary_bottom = platform.center_y
        
        if "moving_danger" in self.scene:
            for platform in self.scene["moving_danger"]:
                platform.boundary_top = platform.center_y + 155
                platform.boundary_bottom = platform.center_y
                
        all_platforms = arcade.SpriteList()
        if "x_moving_platform" in self.scene:
            all_platforms.extend(self.scene["x_moving_platform"])
        if "y_moving_platform" in self.scene:
            all_platforms.extend(self.scene["y_moving_platform"])
        if "moving_danger" in self.scene:
            all_platforms.extend(self.scene["moving_danger"])
                
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, walls=self.scene["Platform"],
            platforms=all_platforms,
            gravity_constant=GRAVITY
        )

        self.camera = arcade.Camera2D(zoom=3)
        self.gui_camera = arcade.Camera2D()

        self.background_color = arcade.csscolor.CORNFLOWER_BLUE


    def on_draw(self):
        self.clear()
        self.camera.use()
        self.scene.draw()
        self.gui_camera.use()
        
        arcade.draw_text(
            f"Lives Remaining: {self.lives}",
            10, WINDOW_HEIGHT - 30,
            font_size = self.font_size,
            color=self.font_color
        )
        
        arcade.draw_text(
            f"Score: {self.score}",
            10, WINDOW_HEIGHT - 60,
            font_size = self.font_size,
            color=self.font_color
        )


    def on_update(self, delta_time):
        self.physics_engine.update()
        self.player_sprite_list.update()
        self.player.update_animation(delta_time)
        
        self.scene.update(delta_time)

        self.camera.position = self.player.position
        
        if "Danger" in self.scene:
            danger_hit_list = arcade.check_for_collision_with_list(self.player, self.scene["Danger"])
            if danger_hit_list:
                self.lives -= 1
                if self.lives > 0:
                    self.player.center_x = self.spawn_x
                    self.player.center_y = self.spawn_x
                    self.player.change_x = 0
                    self.player.change_y = 0
                else:
                    print("Game over")
                    arcade.close_window()
                    
        if "moving_danger" in self.scene:
            moving_danger_hit_list = arcade.check_for_collision_with_list(self.player, self.scene["moving_danger"])
            if moving_danger_hit_list: 
                if moving_danger_hit_list:
                    self.lives -= 1
                    print(self.lives)
                if self.lives > 0:
                    self.player.center_x = self.spawn_x
                    self.player.center_y = self.spawn_x
                    self.player.change_x = 0
                    self.player.change_y = 0
                else:
                    print("Game over")
                    arcade.close_window()
                
        if self.physics_engine.can_jump():
            self.player.jump_count = 0
            
        coin_hit_list = arcade.check_for_collision_with_list(self.player, self.scene["Coins"])
        
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1
            
        diamond_hit_list = arcade.check_for_collision_with_list(self.player, self.scene["Diamond"])
        
        for diamond in diamond_hit_list:
            diamond.remove_from_sprite_lists()
            self.score += 5
            
        if  "Chest" in self.scene:
            chest_hit_list = arcade.check_for_collision_with_list(self.player, self.scene["Chest"])
            if chest_hit_list:
                print(self.score)
                arcade.exit()

        
                
        
            

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.UP, arcade.key.W):
            if self.physics_engine.can_jump():
                self.player.change_y = PLAYER_JUMP_SPEED
                

        elif key in (arcade.key.LEFT, arcade.key.A):
            self.player.change_x = -MOVEMENT_SPEED
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.player.change_x = MOVEMENT_SPEED
        elif key in (arcade.key.ESCAPE, arcade.key.Q):  
            arcade.close_window()
        
        if key in (arcade.key.UP, arcade.key.W):
            if self.player.jump_count < self.player.max_jumps:
                self.player.change_y = PLAYER_JUMP_SPEED
                self.player.jump_count +=1

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.RIGHT, arcade.key.A, arcade.key.D):
            self.player.change_x = 0
    




def main():
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
 