import pygame as pg
import os, math, random, sys 
import src.settings as s
import src.utils as utils
import src.anim_manager as anim_manager
import src.tilemap as tilemap
import src.entity as entities
import src.mouse as m

'''
GAME_ENGINE: VERSION 1.0
'''

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
        self.inputs = [False, False, False, False]

        # ---- CLASSES 
        self.tile_map = None
        self.anim_manager = anim_manager.AnimationManager(f'{s.ANIM_PATH}')
        
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
        self.player = entities.Player(self, [50,50], [s.CELL_SIZE, s.CELL_SIZE], 'player', True)

# ---- INIT PG
pg.init()
screen: pg.display = pg.display.set_mode((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
display: pg.Surface = pg.Surface((s.WIDTH, s.HEIGHT))
clock: pg.time = pg.time.Clock()
        
app = App()
mouse = m.Mouse(app)
tile_map = tilemap.TileMap(app)

# ---- WINDOWS 
def test_game_loop():
    app.load_level('test')

    while True:
        # --------- UPDATE --------- #
        run()
        display.fill(s.TEST_COLOR)

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
def update():
    clock.tick(s.FPS)
    pg.display.set_caption(f'{clock.get_fps()}')
    app.dt = clock.tick(s.FPS)
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
            if e.key == pg.K_a:
                app.inputs[0] = True
            if e.key == pg.K_d:
                app.inputs[1] = True
            if e.key == pg.K_w:
                app.inputs[2] = True
            if e.key == pg.K_s:
                app.inputs[3] = True
        if e.type == pg.KEYUP:
            if e.key == pg.K_a:
                app.inputs[0] = False
            if e.key == pg.K_d:
                app.inputs[1] = False
            if e.key == pg.K_w:
                app.inputs[2] = False
            if e.key == pg.K_s:
                app.inputs[3] = False

def run():
    update()
    check_inputs()

if __name__ == '__main__':
    test_game_loop()
