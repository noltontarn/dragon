import arcade.key

from random import randint

GAME_RUNNING = 0
GAME_OVER = 1

class Model:
    def __init__(self, world, x, y, angle):
        self.world = world
        self.x = x
        self.y = y
        self.angle = 0

    def hit(self, other, hit_size):
        return (abs(self.x - other.x) <= hit_size) and (abs(self.y - other.y) <= hit_size)
        
class Man:
    DIR_UP = 0
    DIR_DOWN = 1
    DIR_RIGHT = 2
    DIR_LEFT = 3
    SPEED = 3
    STATE_ALIVE = 0
    STATE_STEAK = 1
    STATE_EATEN = 2
    def __init__(self, x, y, width, height, direction):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_died = False
        self.state = self.STATE_ALIVE
        self.direction = direction

    def hit(self, dragon):
        return ((abs(self.x - dragon.x) < 50) and
                (abs(self.y - dragon.y) < 50))

    def animate(self, delta_time):
         if self.direction == self.DIR_UP and self.state == self.STATE_ALIVE:
            if self.y > 720:
                self.y = 0
            self.y += self.SPEED
         elif self.direction == self.DIR_DOWN and self.state == self.STATE_ALIVE:
            if self.y < 0:
                self.y = 720
            self.y -= self.SPEED
         elif self.direction == self.DIR_RIGHT and self.state == self.STATE_ALIVE:
            if self.x > 1280:
                self.x = 0
            self.x += self.SPEED
         elif self.direction == self.DIR_LEFT and self.state == self.STATE_ALIVE:
            if self.x < 0:
                self.x = 1280
            self.x -= self.SPEED

class Fire:
    DIR_UP = 0
    DIR_DOWN = 1
    DIR_RIGHT = 2
    DIR_LEFT = 3
    SPEED = 7
    def __init__(self, x, y, width, height, direction):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.direction = direction
        self.is_hit = False

    def hit(self, man):
        return ((abs(self.x - man.x) < 50) and
                (abs(self.y - man.y) < 50))

    def animate(self, delta_time):
         if self.direction == self.DIR_UP:
            self.y += self.SPEED
         elif self.direction == self.DIR_DOWN:
            self.y -= self.SPEED
         elif self.direction == self.DIR_RIGHT:
            self.x += self.SPEED
         elif self.direction == self.DIR_LEFT:
            self.x -= self.SPEED
        
class Dragon(Model):
    DIR_UP = 0
    DIR_DOWN = 1
    DIR_RIGHT = 2
    DIR_LEFT = 3
    SPEED = 0
    def __init__(self, world, x, y):
        super().__init__(world, x, y, 0)
        
        self.direction = self.DIR_UP
        self.angle = 0
 
 
    def switch_direction(self ,direction):
        self.direction = direction
            
    def animate(self, delta_time):
        if self.direction == self.DIR_UP:
            if self.y > self.world.height:
                self.y = 0
            self.y += self.SPEED
        elif self.direction == self.DIR_DOWN:
            if self.y < 0:
                self.y = 720
            self.y += self.SPEED
        elif self.direction == self.DIR_RIGHT:
            if self.x > self.world.width:
                self.x = 0
            self.x += self.SPEED
        elif self.direction == self.DIR_LEFT:
            if self.x < 0:
                self.x = 1280
            self.x += self.SPEED

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.current_state = GAME_RUNNING
        self.dragon = Dragon(self, 640, 360)
        self.men = []
        self.fire = []
        for i in range(2):
            self.men.append(Man(randint(0, 1280), randint(0, 720), 100, 100, randint(0, 3)))
        self.hunger = 100
        self.hunger_speed = 3
        self.number = 2
        self.score = 0
        self.count = 0
        self.total_time = 0
        self.hit_time = 0
        self.hunger_time = 0
        self.hungerspeed_time = 0
        self.spawn_time = 0
        self.spawncount_time = 0
        self.spawn = False
        self.damage = False
        self.stab_sound = arcade.sound.load_sound("sounds/stab.mp3")
        self.crunch_sound = arcade.sound.load_sound("sounds/crunch.mp3")
        self.fire_sound = arcade.sound.load_sound("sounds/fireball.mp3")
        
    def animate(self, delta_time):
        for m in self.men:
            m.animate(delta_time)
        self.dragon.animate(delta_time)
        for f in self.fire:
            f.animate(delta_time)
        self.hit_men()
        self.collect_men()
        self.spawn_men()
        self.total_time += delta_time
        self.deplete_hunger()

    def deplete_hunger(self):
        if self.total_time - self.hungerspeed_time > 30:
            self.hunger_speed += 2
            self.hungerspeed_time = self.total_time
        if self.total_time - self.hunger_time > 2:
            self.hunger -= self.hunger_speed
            self.hunger_time = self.total_time
            if self.hunger < 0:
                self.hunger = 0
                self.current_state = GAME_OVER

    def hit_men(self):
        for m in self.men:
            for f in self.fire:
                if (not m.is_died) and (f.hit(m)) and f.is_hit == False:
                    f.is_hit = True
                    m.is_died = True
                    m.state = m.STATE_STEAK

    def collect_men(self):
        if self.total_time - self.hit_time > 2:
            self.damage = False
        for m in self.men:
            if m.state == m.STATE_STEAK and (m.hit(self.dragon)):
                arcade.sound.play_sound(self.crunch_sound)
                m.state = m.STATE_EATEN
                self.score += 500
                self.count += 1
                self.hunger += 10
                if self.hunger > 100:
                    self.hunger = 100
            if m.state == m.STATE_ALIVE and (m.hit(self.dragon)) and self.damage == False:
                arcade.sound.play_sound(self.stab_sound)
                self.score -= 250
                if self.score < 0:
                    self.score = 0
                self.hunger -= 5
                self.hit_time = self.total_time
                self.damage = True
                if self.hunger < 0:
                    self.hunger = 0
                    self.current_state = GAME_OVER

    def spawn_men(self):
        if self.total_time - self.spawncount_time > 40:
            self.number += 1
            self.spawncount_time = self.total_time
            for m in self.men:
                m.SPEED += 1
        if self.total_time - self.spawn_time > 8:
            self.spawn_time = self.total_time
            for i in range(self.number):
                self.men.append(Man(randint(0, 1280), randint(0, 720), 100, 100, randint(0, 3)))
            
    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.UP:
            self.dragon.switch_direction(self.dragon.DIR_UP)
            self.dragon.SPEED = 5
        elif key == arcade.key.DOWN:
            self.dragon.switch_direction(self.dragon.DIR_DOWN)
            self.dragon.SPEED = -5
        elif key == arcade.key.RIGHT:
            self.dragon.switch_direction(self.dragon.DIR_RIGHT)
            self.dragon.SPEED = 5
        elif key == arcade.key.LEFT:
            self.dragon.switch_direction(self.dragon.DIR_LEFT)
            self.dragon.SPEED = -5
        if key == arcade.key.SPACE:
            arcade.sound.play_sound(self.fire_sound)
            self.fire.append(Fire(self.dragon.x, self.dragon.y, 50, 50, self.dragon.direction))
            self.hunger -= 3
            if self.hunger < 0:
                    self.hunger = 0
                    self.current_state = GAME_OVER

    def on_key_release(self, key, key_modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN or key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.dragon.SPEED = 0

