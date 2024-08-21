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
        # ------- HASH DATA ------- # 
        self.fonts = {
            'basic': f'{set.FONTS_PATH}basic.ttf'
        }

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
        self.tile_id= 0
        self.curr_tile = None

    def render(self):
        self.display.fill((0, 0, 0))

        # --------- HANDLE CURR TILE ---------- #
        if self.tile_type >= 0:
            self.tile_type %= len(self.tile_editor.tile_data)

            if self.tile_name >= 0:
                self.tile_name %= len(self.tile_editor.tile_data[self.tile_type])
            elif self.tile_name < 0:
                self.tile_name = len(self.tile_editor.tile_data[self.tile_type]) - 1

            if self.tile_id >= 0:
                self.tile_id %= len(self.tile_editor.tile_data[self.tile_type][self.tile_name][2])
            elif self.tile_id < 0:
                self.tile_id = len(self.tile_editor.tile_data[self.tile_type][self.tile_name][2]) - 1

        elif self.tile_type < 0:
            self.tile_type = len(self.tile_editor.tile_data) - 1

        ui_data = {
            'tile_type': "NONE",
            'tile_name': "NONE",
            'tile_id': "NONE"
        }

        if self.tile_editor.tile_data[self.tile_type][0][0] in {'tileset', 'bg_tiles', 'decor'}:
            ui_data['tile_type'] = self.tile_editor.tile_data[self.tile_type][0][0]
            ui_data['tile_name'] = self.tile_editor.tile_data[self.tile_type][self.tile_name][1]
            tile_path = self.tile_editor.tile_data[self.tile_type][self.tile_name][2][self.tile_id]
            tile_png = self.tile_editor.tile_data[self.tile_type][self.tile_name][2][self.tile_id].split('/')[-1]
            tile_id = tile_png.split('.')[0]
            ui_data['tile_id'] = tile_id
            tile_config = self.tile_editor.tile_data[self.tile_type][self.tile_name][3][tile_id]

            tile_image = utils.get_image(tile_path, tile_config['size'])
            self.curr_tile = [tile_image]


        # ----- MOUSE ---- #
        mouse_pos = pg.mouse.get_pos()
        self.mouse.pos = [mouse_pos[0]//2, mouse_pos[1]//2]
        self.mouse.update()
        mouse_rect = self.mouse.rect()

        # --------- RENDER ------- # 

        

        if self.curr_tile:
            pg.draw.rect(self.display, set.WHITE, (self.mouse.pos[0], self.mouse.pos[1], set.CELL_SIZE, set.CELL_SIZE), 1)
            self.display.blit(self.curr_tile[0], (self.mouse.pos[0], self.mouse.pos[1]))

        # --------- UI --------- #

        tile_type = ui_data['tile_type']
        tile_name = ui_data['tile_name']
        tile_id = ui_data['tile_id']

        tile_type_text = utils.text_surface_1(f'Type: {tile_type}', 12, False, set.WHITE, font_path=self.fonts['basic'])
        self.display.blit(tile_type_text, [set.WIDTH - tile_type_text.get_width() - 10, 10])

        tile_name_text = utils.text_surface_1(f'Name: {tile_name}', 12, False, set.WHITE, font_path=self.fonts['basic'])
        self.display.blit(tile_name_text, [set.WIDTH - tile_name_text.get_width() - 10, 30])

        tile_id_text = utils.text_surface_1(f'ID: {tile_id}', 12, False, set.WHITE, font_path=self.fonts['basic'])
        self.display.blit(tile_id_text, [set.WIDTH - tile_id_text.get_width() - 10, 50])

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
                if e.key == pg.K_q:
                    self.tile_type -= 1
                if e.key == pg.K_e:
                    self.tile_type += 1
                if e.key == pg.K_a:
                    self.tile_name -= 1 
                if e.key == pg.K_d:
                    self.tile_name += 1

                if e.key == pg.K_w:
                    self.tile_id += 1
                if e.key == pg.K_s:
                    self.tile_id -= 1

                if e.key == pg.K_COMMA:
                    self.layer -= 1
                if e.key == pg.K_PERIOD:
                    self.layer += 1

    def update(self):
        self.clock.tick(set.FPS)
        pg.display.set_caption(f'{self.clock.get_fps()}')
        self.dt = self.clock.tick(set.FPS)
        self.dt /= 1000

    def run(self):
        while True:
            self.render()
            self.update()
            self.check_inputs()

if __name__ == '__main__':
    app = Level_Editor()
    app.run()
