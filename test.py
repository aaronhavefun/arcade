"""
Frog Adventures - A platformer game where the player collects coins and diamonds
while avoiding dangers to achieve financial stability.
"""

import arcade
import os
import random

# Constants for the game
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900
WINDOW_TITLE = "Frog Adventures"

TILE_SCALING = 1
PLAYER_JUMP_SPEED = 3
PLAYER_DOUBLE_JUMP_SPEED = 2
GRAVITY = 0.25

MOVEMENT_SPEED = 0.6
UPDATES_PER_FRAME = 5

RIGHT_FACING = 0
LEFT_FACING = 1

CHARACTER_SCALING = 1
FOLLOW_DECAY_CONST = 0.3

PLAYER_CLIMB_SPEED = 0.5

BULLET_SPEED = -1
BULLET_TEXTURE = "rocky_roads/Enemies/bullet.png"
BULLET_SCALING = 1

QUICKSAND_SPEED_DEBUFF = 0.3


class GameEnd(arcade.View):
    """View displayed when the player completes all levels."""

    def __init__(self, final_score, final_time):
        """
        Initialize the GameEnd view with final score and time.

        Args:
            final_score (int): Player's final score
            final_time (float): Time taken to complete the game
        """
        super().__init__()
        self.final_score = final_score
        self.final_time = f"{final_time:.2f}s"

    def on_show_view(self):
        """Set the background color when the view is shown."""
        self.window.background_color = arcade.color.OLD_GOLD

    def on_draw(self):
        """Render the game end screen with results and options."""
        self.clear()
        arcade.draw_text(
            "You beat the game!\nCongratulations, you are now more financially stable.",
            WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2,
            arcade.color.BLACK,
            font_size=40, anchor_x="center"
        )
        arcade.draw_text(
            f"You beat the game in {self.final_time}, with a score of "
            f"{self.final_score}! Compare with your friends.",
            WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 75,
            arcade.color.BLACK, font_size=25, anchor_x="center"
        )
        arcade.draw_text(
            "Press ENTER to quit, or CLICK anywhere to restart.",
            WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 120,
            arcade.color.BLACK, font_size=25, anchor_x="center"
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """
        Handle mouse press to restart the game.

        Args:
            _x (int): X coordinate of mouse click
            _y (int): Y coordinate of mouse click
            _button (int): Mouse button pressed
            _modifiers (int): Key modifiers
        """
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)

    def on_key_press(self, key, modifiers):
        """
        Handle key press to exit the game.

        Args:
            key (int): Key code pressed
            modifiers (int): Key modifiers
        """
        if key == arcade.key.ENTER:
            arcade.exit()


class MenuView(arcade.View):
    """Main menu view displayed when the game starts."""

    def on_show_view(self):
        """Set the background color when the view is shown."""
        self.window.background_color = arcade.color.COSMIC_LATTE

    def on_draw(self):
        """Render the menu screen."""
        self.clear()
        arcade.draw_text(
            "Welcome to Frog Adventures",
            WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2,
            arcade.color.BLACK, font_size=50, anchor_x="center"
        )
        arcade.draw_text(
            "Click to advance",
            WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 75,
            arcade.color.GRAY, font_size=25, anchor_x="center"
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """
        Handle mouse press to advance to instructions.

        Args:
            _x (int): X coordinate of mouse click
            _y (int): Y coordinate of mouse click
            _button (int): Mouse button pressed
            _modifiers (int): Key modifiers
        """
        instruction_view = InstructionView()
        self.window.show_view(instruction_view)


class InstructionView(arcade.View):
    """View displaying game instructions."""

    def on_show_view(self):
        """Set the background color when the view is shown."""
        self.window.background_color = arcade.color.GO_GREEN

    def on_draw(self):
        """Render the instruction screen."""
        self.clear()
        arcade.draw_text(
            "You are a Frog, collect as many diamonds and coins in the shortest "
            "time\n to be most successful in the future.",
            WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2,
            arcade.color.BLACK, font_size=25, anchor_x="center"
        )
        arcade.draw_text(
            "A/D to move left and right, Space/W to jump, and double tap jump "
            "to double jump.",
            WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 75,
            arcade.color.GRAY, font_size=20, anchor_x="center"
        )
        arcade.draw_text(
            "Click to advance",
            WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 175,
            arcade.color.GRAY, font_size=20, anchor_x="center"
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """
        Handle mouse press to start the game.

        Args:
            _x (int): X coordinate of mouse click
            _y (int): Y coordinate of mouse click
            _button (int): Mouse button pressed
            _modifiers (int): Key modifiers
        """
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


class GameOverView(arcade.View):
    """View displayed when the player loses all lives."""

    def __init__(self, final_score, final_time):
        """
        Initialize the GameOver view with final score and time.

        Args:
            final_score (int): Player's final score
            final_time (float): Time taken before game over
        """
        super().__init__()
        self.final_score = final_score
        self.final_time = f"{final_time:.2f}s"

    def on_show_view(self):
        """Set the background color when the view is shown."""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """Render the game over screen."""
        self.clear()
        arcade.draw_text(
            "Game Over",
            WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 100,
            arcade.color.RED, 60, anchor_x="center"
        )
        arcade.draw_text(
            f"Final Score and Time: {self.final_score}pts and {self.final_time}.",
            WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 25,
            arcade.color.RED, 60, anchor_x="center"
        )
        arcade.draw_text(
            f"Click to restart, or ENTER to quit.",
            WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 150,
            arcade.color.RED, 60, anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        """
        Handle key press to exit the game.

        Args:
            key (int): Key code pressed
            modifiers (int): Key modifiers
        """
        if key == arcade.key.ENTER:
            arcade.exit()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """
        Handle mouse press to restart the game.

        Args:
            _x (int): X coordinate of mouse click
            _y (int): Y coordinate of mouse click
            _button (int): Mouse button pressed
            _modifiers (int): Key modifiers
        """
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


class PlayerCharacter(arcade.Sprite):
    """Player character sprite with animation capabilities."""

    def __init__(self, idle_texture_pairs, walk_texture_pairs, jump_texture_pairs):
        """
        Initialize the player character.

        Args:
            idle_texture_pairs (list): Textures for idle animation
            walk_texture_pairs (list): Textures for walking animation
            jump_texture_pairs (list): Textures for jumping animation
        """
        self.character_face_direction = RIGHT_FACING
        self.cur_texture = 0

        self.idle_texture_pairs = idle_texture_pairs
        self.walk_textures = walk_texture_pairs
        self.jump_texture_pairs = jump_texture_pairs

        super().__init__(self.idle_texture_pairs[0], scale=CHARACTER_SCALING)

        self.jump_count = 0
        self.max_jumps = 2

    def update_animation(self, delta_time: float = 1 / 60):
        """Update the player's animation based on current state."""
        if self.change_x < 0:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0:
            self.character_face_direction = RIGHT_FACING

        if self.change_y > 0:
            self.cur_texture += 1
            if self.cur_texture >= len(self.jump_texture_pairs) * UPDATES_PER_FRAME:
                self.cur_texture = 0
            frame = self.cur_texture // UPDATES_PER_FRAME
            direction = self.character_face_direction
            self.texture = self.jump_texture_pairs[frame][direction]
            return

        if self.change_x == 0:
            self.cur_texture += 1
            if self.cur_texture >= len(self.idle_texture_pairs) * UPDATES_PER_FRAME:
                self.cur_texture = 0
            frame = self.cur_texture // UPDATES_PER_FRAME
            direction = self.character_face_direction
            self.texture = self.idle_texture_pairs[frame][direction]
            return

        self.cur_texture += 1
        if self.cur_texture >= 8 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        frame = self.cur_texture // UPDATES_PER_FRAME
        direction = self.character_face_direction
        self.texture = self.walk_textures[frame][direction]


class Bullet(arcade.Sprite):
    """Projectile sprite fired by cannons."""

    def __init__(self, filename, scale):
        """
        Initialize a bullet sprite.

        Args:
            filename (str): Path to bullet texture
            scale (float): Scaling factor for the sprite
        """
        super().__init__(filename, scale)
        self.should_be_removed = False

    def update(self, delta_time: float = 1/60):
        """
        Update bullet position and check if it should be removed.

        Args:
            delta_time (float): Time since last update
        """
        super().update()
        if (self.right < 0 or self.left > WINDOW_WIDTH or
                self.bottom < 0 or self.top > WINDOW_HEIGHT):
            self.should_be_removed = True


class GameView(arcade.View):
    """Main game view where gameplay occurs."""

    def __init__(self):
        """Initialize the game view."""
        super().__init__()

        self.tile_map = None
        self.scene = None
        self.camera = None
        self.gui_camera = None
        self.player_sprite_list = None
        self.physics_engine = None

        self.player = None

        self.lives = 5
        self.font_size = 20
        self.font_color = arcade.color.WHITE

        self.score = 0
        self.level = 1
        self.time_taken = 0

        self.view_bottom = 0
        self.view_left = 0

        character = "frog_man/frog_man"

        self.idle_texture_pairs = []
        for i in range(8):
            texture = arcade.load_texture(f"{character}_idle{i}.png")
            self.idle_texture_pairs.append((texture, texture.flip_left_right()))

        self.walk_texture_pairs = []
        for i in range(8):
            texture = arcade.load_texture(f"{character}_walk{i}.png")
            self.walk_texture_pairs.append((texture, texture.flip_left_right()))

        self.jump_texture_pairs = []
        for i in range(2):
            texture = arcade.load_texture(f"{character}_jump{i}.png")
            self.jump_texture_pairs.append((texture, texture.flip_left_right()))

        self.bullet_list = arcade.SpriteList()
        self.cannon_fire_timers = {}
        
        self.is_on_quicksand = False
        self.current_movement_speed = MOVEMENT_SPEED

    def setup(self):
        """Set up the game level with platforms, enemies, and collectibles."""
        layer_options = {
            "Platform": {"use_spatial_hash": True},
            "Coins": {"use_spatial_hash": True},
            "Danger": {"use_spatial_hash": True},
            "Diamond": {"use_spatial_hash": True},
            "x_moving_platform": {"use_spatial_hash": True},
            "y_moving_platform": {"use_spatial_hash": True},
            "moving_danger": {"use_spatial_hash": True},
            "Bounce": {"use_spatial_hash": True},
            "Quicksand": {"use_spatial_hash": True},
            "CrabEnemy": {"use_spatial_hash": True}
        }

        map_path = os.path.join(os.path.dirname(__file__), "level3.tmx")

        self.tile_map = arcade.load_tilemap(
            map_path,
            scaling=TILE_SCALING,
            layer_options=layer_options,
        )

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        zoom_level = 3
        self.camera = arcade.Camera2D()
        self.camera.zoom = zoom_level

        map_width_pixels = self.tile_map.width * self.tile_map.tile_width
        map_height_pixels = self.tile_map.height * self.tile_map.tile_height

        half_screen_width = (self.window.width / 2) / zoom_level
        half_screen_height = (self.window.height / 2) / zoom_level

        self.camera_bounds = arcade.LRBT(
            left=half_screen_width,
            right=map_width_pixels - half_screen_width,
            bottom=half_screen_height,
            top=map_height_pixels - half_screen_height
        )

        self.player_sprite_list = arcade.SpriteList()

        self.player = PlayerCharacter(
            self.idle_texture_pairs,
            self.walk_texture_pairs,
            self.jump_texture_pairs,
        )
        self.player.center_x = 50
        self.player.center_y = 160
        self.spawn_x = self.player.center_x
        self.spawn_y = self.player.center_y
        self.player_sprite_list.append(self.player)
        self.scene.add_sprite("Player", self.player)
        self.scene.add_sprite_list_before("Foreground", "Player")

        self.moving_danger_list = arcade.SpriteList()
        self.cannon_list = arcade.SpriteList()
        self.bounce_list = arcade.SpriteList()
        self.crab_enemy_list = arcade.SpriteList()
        
        if "Bounce" in self.scene:
            self.bounce_list = self.scene["Bounce"]

        if "Cannon" in self.scene:
            self.cannon_list = self.scene["Cannon"]

        if "moving_danger" in self.scene:
            self.moving_danger_list = self.scene["moving_danger"]
            
        if "CrabEnemy" in self.scene:
            self.crab_enemy_list = self.scene["CrabEnemy"]

        self.jump_key_pressed = False

        self.ladder_list = (self.scene["Ladder"] if "Ladder" in self.scene
                           else arcade.SpriteList())

        if "x_moving_platform" in self.scene:
            for platform in self.scene["x_moving_platform"]:
                platform.boundary_left = platform.center_x
                platform.boundary_right = platform.center_x + 260

        if "y_moving_platform" in self.scene:
            for platform in self.scene["y_moving_platform"]:
                platform.boundary_top = platform.center_y + 400
                platform.boundary_bottom = platform.center_y

        if "moving_danger" in self.scene:
            for platform in self.scene["moving_danger"]:
                platform.boundary_top = platform.center_y + 155
                platform.boundary_bottom = platform.center_y

        if "UpMovingPlatforms" in self.scene:
            for platform in self.scene["UpMovingPlatforms"]:
                platform.boundary_top = platform.center_y + 400
                platform.boundary_bottom = platform.center_y

        if "DownMovingPlatforms" in self.scene:
            for platform in self.scene["DownMovingPlatforms"]:
                platform.boundary_top = platform.center_y
                platform.boundary_bottom = platform.center_y - 400
                
        if "CrabEnemy" in self.scene: 
            for enemy in self.scene["CrabEnemy"]:
                enemy.boundary_left = enemy.center_x
                enemy.boundary_right = enemy.center_x + 250

        all_platforms = arcade.SpriteList()
        if "x_moving_platform" in self.scene:
            all_platforms.extend(self.scene["x_moving_platform"])
        if "y_moving_platform" in self.scene:
            all_platforms.extend(self.scene["y_moving_platform"])
        if "moving_danger" in self.scene:
            all_platforms.extend(self.scene["moving_danger"])
        if "UpMovingPlatforms" in self.scene:
            all_platforms.extend(self.scene["UpMovingPlatforms"])
        if "DownMovingPlatforms" in self.scene:
            all_platforms.extend(self.scene["DownMovingPlatforms"])
        if "CrabEnemy" in self.scene:
            all_platforms.extend(self.scene["CrabEnemy"])
            
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            walls=self.scene["Platform"],
            platforms=all_platforms,
            gravity_constant=GRAVITY
        )

        self.gui_camera = arcade.Camera2D()
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE
        self.camera.zoom = 3
        
        if "Cannon" in self.scene:
            for cannon in self.scene["Cannon"]:
                self.cannon_fire_timers[cannon] = random.uniform(1, 50)

    def on_draw(self):
        """Render the game screen."""
        self.clear()
        self.camera.use()
        self.scene.draw()
        self.bullet_list.draw()
        self.gui_camera.use()

        arcade.draw_text(
            f"Lives Remaining: {self.lives}",
            10, WINDOW_HEIGHT - 30,
            font_size=self.font_size,
            color=self.font_color
        )

        arcade.draw_text(
            f"Score: {self.score}",
            10, WINDOW_HEIGHT - 60,
            font_size=self.font_size,
            color=self.font_color
        )

        arcade.draw_text(
            f"Time Taken: {self.time_taken:.2f}",
            10, WINDOW_HEIGHT - 90,
            font_size=self.font_size,
            color=self.font_color
        )

    def center_camera_to_player(self):
        """Center the camera on the player with smooth following."""
        self.camera.position = arcade.math.smerp_2d(
            self.camera.position,
            self.player.position,
            self.window.delta_time,
            FOLLOW_DECAY_CONST,
        )
        self.camera.view_data.position = arcade.camera.grips.constrain_xy(
            self.camera.view_data, self.camera_bounds
        )

    def on_resize(self, width: int, height: int):
        """
        Handle window resize events.

        Args:
            width (int): New window width
            height (int): New window height
        """
        super().on_resize(width, height)
        self.camera.match_window()
        self.gui_camera.match_window(position=True)

    def on_update(self, delta_time):
        """Update game state and handle collisions."""
        self.physics_engine.update()
        self.player_sprite_list.update()
        self.player.update_animation(delta_time)
        self.scene["Coins"].update_animation(delta_time)
        self.scene["Diamond"].update_animation(delta_time)
        self.moving_danger_list.update_animation(delta_time)
        self.cannon_list.update_animation(delta_time)
        self.scene["Danger"].update_animation(delta_time)
        self.scene["CrabEnemy"].update_animation(delta_time)
        self.scene.update(delta_time)

        self.time_taken += delta_time
        self.center_camera_to_player()

        map_left = 0
        map_right = self.tile_map.width * self.tile_map.tile_width

        if self.player.left < map_left:
            self.player.left = map_left
        elif self.player.right > map_right:
            self.player.right = map_right

        is_on_ladder = arcade.check_for_collision_with_list(
            self.player, self.ladder_list
        )

        if is_on_ladder:
            self.player.change_y = 0
            if self.jump_key_pressed:
                self.player.change_y = PLAYER_CLIMB_SPEED
        
        if "Danger" in self.scene:
            danger_hit_list = arcade.check_for_collision_with_list(
                self.player, self.scene["Danger"]
            )
            if danger_hit_list:
                self.player_dies()

        if "moving_danger" in self.scene:
            moving_danger_hit_list = arcade.check_for_collision_with_list(
                self.player, self.scene["moving_danger"]
            )
            if moving_danger_hit_list:
                self.player_dies()
                
        if "CrabEnemy" in self.scene:
            crab_enemy_hit_list = arcade.check_for_collision_with_list(
                self.player, self.scene["CrabEnemy"]
            )
            if crab_enemy_hit_list:
                self.player_dies()
                
        if "Bounce" in self.scene:
            bounce_hit_list = arcade.check_for_collision_with_list(
                self.player, self.scene["Bounce"]
            )
            if bounce_hit_list:
                self.player.change_y = 10
                self.player.jump_count = 1
                
        quicksand_hit_list = []
        if "Quicksand" in self.scene:
            quicksand_hit_list = arcade.check_for_collision_with_list(
                self.player, self.scene["Quicksand"]
            )
            
        if quicksand_hit_list:
            if not self.is_on_quicksand:
                self.is_on_quicksand = True
                self.current_movement_speed = MOVEMENT_SPEED * QUICKSAND_SPEED_DEBUFF
                
            if self.player.change_x != 0:
                self.player.change_x = (self.player.change_x / abs(self.player.change_x) 
                                      * self.current_movement_speed)
        else:
            if self.is_on_quicksand:
                self.is_on_quicksand = False
                self.current_movement_speed = MOVEMENT_SPEED
                
                if self.player.change_x != 0:
                    self.player.change_x = (self.player.change_x / abs(self.player.change_x) 
                                          * self.current_movement_speed)
        
        self.bullet_list.update(delta_time)
        
        for bullet in self.bullet_list:
            if bullet.should_be_removed:
                bullet.remove_from_sprite_lists()

        bullet_hit_list = arcade.check_for_collision_with_list(
            self.player, self.bullet_list
        )
        for bullet in bullet_hit_list:
            bullet.remove_from_sprite_lists()
            self.player_dies()

        if "Cannon" in self.scene:
            for cannon in self.scene["Cannon"]:
                self.cannon_fire_timers[cannon] -= delta_time
                if self.cannon_fire_timers[cannon] <= 0:
                    self.fire_bullet_from_cannon(cannon)
                    self.cannon_fire_timers[cannon] = random.uniform(1, 10)

        if self.physics_engine.can_jump():
            self.player.jump_count = 0

        coin_hit_list = arcade.check_for_collision_with_list(
            self.player, self.scene["Coins"]
        )
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1

        diamond_hit_list = arcade.check_for_collision_with_list(
            self.player, self.scene["Diamond"]
        )
        for diamond in diamond_hit_list:
            diamond.remove_from_sprite_lists()
            self.score += 5

        if "Chest" in self.scene:
            chest_hit_list = arcade.check_for_collision_with_list(
                self.player, self.scene["Chest"]
            )
            if chest_hit_list:
                self.level += 1
                self.setup()
                
        if "Final" in self.scene:
            final_chest_hit_list = arcade.check_for_collision_with_list(
                self.player, self.scene["Final"]
            )
            if final_chest_hit_list:
                game_end = GameEnd(self.score, self.time_taken)
                self.window.show_view(game_end)

    def player_dies(self):
        """Handle player death and check for game over."""
        self.lives -= 1
        if self.lives > 0:
            self.player.center_x = self.spawn_x
            self.player.center_y = self.spawn_y
            self.player.change_y = 0
        else:
            game_over_view = GameOverView(self.score, self.time_taken)
            self.window.show_view(game_over_view)

    def fire_bullet_from_cannon(self, cannon):
        """
        Fire a bullet from a cannon.

        Args:
            cannon (arcade.Sprite): Cannon sprite firing the bullet
        """
        bullet = Bullet(BULLET_TEXTURE, BULLET_SCALING)
        bullet.center_x = cannon.center_x
        bullet.center_y = cannon.center_y
        bullet.change_x = BULLET_SPEED
        self.bullet_list.append(bullet)

    def on_key_press(self, key, modifiers):
        """
        Handle keyboard input for player movement.

        Args:
            key (int): Key code pressed
            modifiers (int): Key modifiers
        """
        if key in (arcade.key.W, arcade.key.SPACE):
            if self.physics_engine.can_jump():
                self.player.change_y = PLAYER_JUMP_SPEED
                self.player.jump_count = 1
            elif self.player.jump_count == 1:
                self.player.change_y = PLAYER_DOUBLE_JUMP_SPEED
                self.player.jump_count += 1
        elif key in (arcade.key.LEFT, arcade.key.A):
            self.player.change_x = -self.current_movement_speed
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.player.change_x = self.current_movement_speed
        elif key in (arcade.key.ESCAPE, arcade.key.Q):
            arcade.close_window()

        if key == arcade.key.W or key == arcade.key.SPACE:
            self.jump_key_pressed = True

    def on_key_release(self, key, modifiers):
        """
        Handle key release for stopping movement.

        Args:
            key (int): Key code released
            modifiers (int): Key modifiers
        """
        if key in (arcade.key.LEFT, arcade.key.RIGHT, arcade.key.A, arcade.key.D):
            self.player.change_x = 0

        if key == arcade.key.W or key == arcade.key.SPACE:
            self.jump_key_pressed = False


def main():
    """Main function to start the game."""
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()