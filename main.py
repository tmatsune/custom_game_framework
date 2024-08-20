import pygame as pg
import os, math, random, sys 
import src.settings as set
import src.utils as utils
import src.anim_manager as anim_manager
import src.tilemap as tilemap
import src.entity as entities

class App:
    def __init__(self) -> None:
        # ---- VARS
        self.dt = 0 
        self.screenshake = 0 
        self.total_time = 0 
        self.level = None

        # ---- LIST VARS
        self.particles = []
        self.projectiles = [] 
        self.circles = []
        self.circle_particles = [] 
        self.offset = [0,0] 

        # ---- CLASSES 
        self.tile_map = None
        self.anim_manager = anim_manager.AnimationManager(f'{set.ANIM_PATH}')
        
        # ---- ENTITIES    
        self.player = None
        self.entities = [] 

    def load_spawn_points(self, level_data):
        pass
    def load_level_data(self, level):
        pass
    def load_level(self, level):
        level_data = self.load_level_data(level)
        spawn_points = self.load_spawn_points(level_data)
        self.player = entities.Player(self, [50,100], [set.CELL_SIZE, set.CELL_SIZE], 'player', True)

# ---- INIT PG
pg.init()
screen: pg.display = pg.display.set_mode((set.SCREEN_WIDTH, set.SCREEN_HEIGHT))
display: pg.Surface = pg.Surface((set.WIDTH, set.HEIGHT))
clock: pg.time = pg.time.Clock()
        
app = App()
tile_map = tilemap.TileMap(app)

# ---- WINDOWS 
def test_game_loop():
    app.load_level('test')

    while True:
        # --------- UPDATE --------- #
        run(app)
        display.fill(set.TEST_COLOR)

        # --------- PLAYER --------- #
        app.player.update()
        app.player.render(display)



        # ------ BLIT SCREENS ------ #
        screenshake_offset = [0,0]
        if app.screenshake > 0:
            app.screenshake -= 1
            screenshake_offset[0] = random.randrange(-8, 8)
            screenshake_offset[1] = random.randrange(-8, 8)

        screen.blit(pg.transform.scale(display, screen.get_size()),(0 + screenshake_offset[0], 0 + screenshake_offset[1]))
        pg.display.flip()
        pg.display.update()

def menu_loop():
    pass

def main_game_loop():
    pass

# ---- MAIN PG FUNCS
def update(app):
    clock.tick(set.FPS)
    pg.display.set_caption(f'{clock.get_fps()}')
    app.dt = clock.tick(set.FPS)
    app.dt /= 1000

def check_inputs():
    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_1:
                pg.quit()
                sys.exit()

def run(app):
    update(app)
    check_inputs()

if __name__ == '__main__':
    test_game_loop()
