import pygame as pg, sys
import src.mouse as m
import src.settings as set
import src.utils as utils 
import src.tilemap as tilemap


class Level_Editor:
    def __init__(self) -> None:
        pg.init()
        # ------ PG DATA ------ #
        self.screen: pg.display = pg.display.set_mode((set.SCREEN_WIDTH, set.SCREEN_HEIGHT))
        self.display: pg.Surface = pg.Surface((set.WIDTH, set.HEIGHT))
        self.dt: float = 0
        self.clock: pg.time = pg.time.Clock()

        # ------- LIST DATA ------ #
        self.inputs = [False, False, False, False]
        self.offset = [0, 0]

        # ------ VARS ------ #
        self.left_clicked = False
        self.right_clicked = False
        self.tile_index = 0
        self.tile_img_index = 0
        self.curr_map_id = -1
        self.layer = 0 
        self.curr_tile = None

        # ----- CLASSES ----- #
        self.mouse = m.Mouse(self)
        pg.mouse.set_visible(False)
        self.tile_editor = tilemap.Tile_Editor(self)


    def render(self):

        self.display.fill((0, 0, 0))

        # ----- MOUSE ---- #
        mouse_pos = pg.mouse.get_pos()
        self.mouse.pos = [mouse_pos[0]//2, mouse_pos[1]//2]
        self.mouse.update()
        mouse_rect = self.mouse.rect()

        # ----- BLIT SCREENS ----- #
        self.mouse.render(self.display)
        self.screen.blit(pg.transform.scale(self.display, self.screen.get_size()), (0, 0))
        pg.display.flip()
        pg.display.update()

    def check_inputs(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

    def update(self):
        self.clock.tick(set.FPS)
        pg.display.set_caption(f'{self.clock.get_fps()}')
        self.dt = self.clock.tick(set.FPS)
        self.dt /= 1000

    def run(self):
        while True:
            self.check_inputs()
            self.render()
            self.update()

if __name__ == '__main__':
    app = Level_Editor()
    app.run()
