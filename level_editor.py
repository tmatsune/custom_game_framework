import pygame as pg, sys
import src.mouse as m
import src.settings as s
import src.utils as utils 
import src.tilemap as tilemap


class Level_Editor:
    def __init__(self) -> None:
        pg.init()
        # ------ PG DATA ------ #
        self.screen: pg.display = pg.display.set_mode((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
        self.display: pg.Surface = pg.Surface((s.WIDTH, s.HEIGHT))
        self.dt: float = 0
        self.clock: pg.time = pg.time.Clock()

        # ------- LIST DATA ------ #
        self.inputs = [False, False, False, False]
        self.offset = [0, 0]
        # ------- HASH DATA ------- # 
        self.fonts = {
            'basic': f'{s.FONTS_PATH}basic.ttf'
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

        # --------- MAIN RENDER ACTIONS ---------- #

        self.offset[0] += (self.inputs[1] - self.inputs[0]) * s.CELL_SIZE
        self.offset[1] += (self.inputs[3] - self.inputs[2]) * s.CELL_SIZE

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
            tile_type = self.tile_editor.tile_data[self.tile_type][0][0]
            tile_name = self.tile_editor.tile_data[self.tile_type][self.tile_name][1]
            ui_data['tile_type'] = tile_type
            ui_data['tile_name'] = tile_name
            tile_path = self.tile_editor.tile_data[self.tile_type][self.tile_name][2][self.tile_id]
            tile_png = self.tile_editor.tile_data[self.tile_type][self.tile_name][2][self.tile_id].split('/')[-1]
            tile_id = tile_png.split('.')[0]
            ui_data['tile_id'] = tile_id
            tile_config = self.tile_editor.tile_data[self.tile_type][self.tile_name][3][tile_id]

            tile_image = utils.get_image(tile_path, tile_config['size'])
            self.curr_tile = [tile_type, tile_name, tile_id, tile_path, tile_image]

        # ----- MOUSE ---- #
        mouse_pos = pg.mouse.get_pos()
        self.mouse.pos = [mouse_pos[0]//2, mouse_pos[1]//2]
        self.mouse.update()
        mouse_rect = self.mouse.rect()

        # --------- RENDER ------- # 

        self.tile_editor.test_render(self.display, self.offset)

        if self.curr_tile:
            pg.draw.rect(self.display, s.WHITE, (self.mouse.pos[0], self.mouse.pos[1], s.CELL_SIZE, s.CELL_SIZE), 1)
            self.display.blit(self.curr_tile[-1], (self.mouse.pos[0], self.mouse.pos[1]))

        # --------- ADDING/REMOVING TILES --------- #

        tile_pos = [(self.mouse.pos[0] + self.offset[0]) // s.CELL_SIZE, (self.mouse.pos[1] + self.offset[1]) // s.CELL_SIZE]
        if self.mouse.left_click == m.Click.JUST_PRESSED or self.mouse.left_click == m.Click.PRESSED:
            self.tile_editor.add_tile(tile_pos, self.curr_tile, self.layer)
        if self.mouse.right_click == m.Click.JUST_PRESSED or self.right_clicked == m.Click.PRESSED:
            self.tile_editor.remove_tile(tile_pos, self.layer)

        # --------- UI --------- #
        tile_type = ui_data['tile_type']
        tile_name = ui_data['tile_name']
        tile_id = ui_data['tile_id']

        tile_type_text = utils.text_surface_1(f'Type: {tile_type}', 12, False, s.WHITE, font_path=self.fonts['basic'])
        self.display.blit(tile_type_text, [s.WIDTH - tile_type_text.get_width() - 10, 10])

        tile_name_text = utils.text_surface_1(f'Name: {tile_name}', 12, False, s.WHITE, font_path=self.fonts['basic'])
        self.display.blit(tile_name_text, [s.WIDTH - tile_name_text.get_width() - 10, 30])

        tile_id_text = utils.text_surface_1(f'ID: {tile_id}', 12, False, s.WHITE, font_path=self.fonts['basic'])
        self.display.blit(tile_id_text, [s.WIDTH - tile_id_text.get_width() - 10, 50])

        layer_text = utils.text_surface_1(f'Layer: {self.layer}', 12, False, s.WHITE, font_path=self.fonts['basic'])
        self.display.blit(layer_text, [10, 30])

        top_left_pos_text = utils.text_surface_1(f'{tile_pos[0]},{tile_pos[1]}', 12, False, s.WHITE, font_path=self.fonts['basic'])
        self.display.blit(top_left_pos_text, [10, 10])

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
                if e.key == pg.K_f:
                    if self.curr_tile:
                        tile_imgs = self.tile_editor.tile_data[self.tile_type][self.tile_name][2]
                        tile_pos = [(self.mouse.pos[0] + self.offset[0]) // s.CELL_SIZE,
                                    (self.mouse.pos[1] + self.offset[1]) // s.CELL_SIZE]
                        self.tile_editor.auto_tile(tile_pos, tile_imgs, self.layer)

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

                if e.key == pg.K_LEFT:
                    self.inputs[0] = True
                if e.key == pg.K_RIGHT:
                    self.inputs[1] = True 
                if e.key == pg.K_UP:
                    self.inputs[2] = True
                if e.key == pg.K_DOWN:
                    self.inputs[3] = True

            if e.type == pg.KEYUP:
                if e.key == pg.K_LEFT:
                    self.inputs[0] = False
                if e.key == pg.K_RIGHT:
                    self.inputs[1] = False
                if e.key == pg.K_UP:
                    self.inputs[2] = False
                if e.key == pg.K_DOWN:
                    self.inputs[3] = False
    

            if e.type == pg.MOUSEBUTTONDOWN:
                if e.button == 1:
                    self.left_clicked = True
                if e.button == 3:
                    self.right_clicked = True
            if e.type == pg.MOUSEBUTTONUP:
                if e.button == 1:
                    self.left_clicked = False
                if e.button == 3:
                    self.right_clicked = False

    def update(self):
        self.clock.tick(s.FPS)
        pg.display.set_caption(f'{self.clock.get_fps()}')
        self.dt = self.clock.tick(s.FPS)
        self.dt /= 1000

    def run(self):
        while True:
            self.render()
            self.update()
            self.check_inputs()

if __name__ == '__main__':
    app = Level_Editor()
    app.run()
