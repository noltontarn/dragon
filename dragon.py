import arcade

from models import World, Dragon

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

GAME_RUNNING = 0
GAME_OVER = 1

class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)
 
        super().__init__(*args, **kwargs)
 
    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)
            self.angle = self.model.angle
 
    def draw(self):
        self.sync_with_model()
        super().draw()
        
class DragonGameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.setup(width, height)

    def setup(self, width, height):
        arcade.set_background_color(arcade.color.BLACK)
        self.world = World(width, height)
        self.background_texture = arcade.load_texture('images/background.png')
        self.dragon_sprite = ModelSprite('images/dragon.png',model=self.world.dragon)
        self.man_texture = arcade.load_texture('images/man.png')
        self.steak_texture = arcade.load_texture('images/steak.png')
        self.fire_texture = arcade.load_texture('images/fire.png')
        self.bgm_sound = arcade.sound.load_sound("sounds/sound2.mp3")
        arcade.sound.play_sound(self.bgm_sound)
        
    def draw_men(self, men):
        for m in men:
            if m.state == m.STATE_ALIVE:
                arcade.draw_texture_rectangle(m.x, m.y, m.width, m.height,
                                              self.man_texture)
            if m.state == m.STATE_STEAK:
                arcade.draw_texture_rectangle(m.x, m.y, m.width, m.height,
                                              self.steak_texture)

    def draw_fire(self, fire):
        for f in fire:
            if not f.is_hit:
                arcade.draw_texture_rectangle(f.x, f.y, f.width, f.height,
                                              self.fire_texture)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(640, 360, 1280, 720,
                                              self.background_texture)
        self.draw_men(self.world.men)
        self.draw_fire(self.world.fire)
        self.dragon_sprite.draw()
        minutes = int(self.world.total_time) // 60
        seconds = int(self.world.total_time) % 60

        output = "Time: {:02d}:{:02d}".format(minutes, seconds)
        arcade.draw_text(output, 0, 690, arcade.color.WHITE, 20)
        
        arcade.draw_text(str("HUNGER: "),
                         self.width - 550, self.height - 30,
                         arcade.color.WHITE, 20)
        arcade.draw_text(str(self.world.hunger),
                         self.width - 430, self.height - 30,
                         arcade.color.WHITE, 20)
        arcade.draw_text(str("/100"),
                         self.width - 380, self.height - 30,
                         arcade.color.WHITE, 20)

        arcade.draw_text(str("SCORE: "),
                         self.width - 300, self.height - 30,
                         arcade.color.WHITE, 20)
        arcade.draw_text(str(self.world.score),
                         self.width - 200, self.height - 30,
                         arcade.color.WHITE, 20)

        if self.world.current_state == GAME_OVER:
            output = "Game Over"
            arcade.draw_text("Game Over", 440, 360, arcade.color.WHITE, 70)
            arcade.draw_text("Click to restart.", 445, 250, arcade.color.WHITE, 50)
            
    def animate(self, delta_time):
        if self.world.current_state == GAME_RUNNING:
            self.world.animate(delta_time)
        
    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)

    def on_key_release(self, key, key_modifiers):
        self.world.on_key_release(key, key_modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.world.current_state == GAME_OVER:
            self.setup(1280, 720)

if __name__ == '__main__':
    window = DragonGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
