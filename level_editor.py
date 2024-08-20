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
        self.curr_map = None
        self.layer = 0

        # ----- CLASSES ----- #
        self.mouse = m.Mouse(self)
        pg.mouse.set_visible(False)
        self.tile_editor = tilemap.Tile_Editor(self)

        # ------ CURR TILE ----- #
        self.tile_type = 0 
        self.tile_name = 0
        self.tile_img_index = 0
        self.curr_tile = None

    def render(self):
        self.display.fill((0, 0, 0))

        # --------- HANDLE CURR TILE ---------- #
        if self.tile_type > 0:
            self.tile_type %= len(self.tile_editor.tile_data)


        elif self.tile_type < 0:
            self.tile_type = len(self.tile_editor.tile_data) - 1

        ui_hash = {
            'tile_type': None,
            'tile_name': "TODO",
            'tile_id': "TODO"
        }
        if self.tile_editor.tile_data[self.tile_type][0][0] in {'tileset', 'bg_tiles'}:
            print(f'{self.tile_editor.tile_data[self.tile_type][0][0]} have same config in tile_folder(tile_name)')
            print(f'tile type: [{self.tile_type}, {self.tile_editor.tile_data[self.tile_type][0][0]}]')
        elif self.tile_editor.tile_data[self.tile_type][0][0] in {'decor'}:
            print(f'{self.tile_editor.tile_data[self.tile_type][0][0]} each tile in folder(tile_name) has their own custom config')
            print(f'tile type: [{self.tile_type}, {self.tile_editor.tile_data[self.tile_type][0][0]}]')

        # ----- MOUSE ---- #
        mouse_pos = pg.mouse.get_pos()
        self.mouse.pos = [mouse_pos[0]//2, mouse_pos[1]//2]
        self.mouse.update()
        mouse_rect = self.mouse.rect()

        # --------- UI --------- #

        tile_type_text = utils.text_surface(f'type: {tile_type}', 10, False, set.WHITE)
        self.display.blit(tile_type_text, [set.WIDTH - tile_type_text.get_width() - 10, 10])

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
                if e.key == pg.K_COMMA:
                    self.tile_type -= 1
                if e.key == pg.K_PERIOD:
                    self.tile_type += 1

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
