import pygame as pg, os, json
import src.settings as s
import src.utils as utils 

hitable_tilesets = {'tileset_0', 'tileset_1', 'tileset_2'}

# ------- AUTOTILE ------- #
top_left = 0
top_center = 1
top_right = 2
mid_left = 3
mid_center = 4
mid_right = 5
bottom_left = 6
bottom_center = 7
bottom_right = 8
auto_tile_config: dict = {
    ((0, 1), (1, 0)): top_left,
    ((-1, 0), (0, 1), (1, 0)): top_center,
    ((-1, 0), (0, 1)): top_right,
    ((0, -1), (0, 1), (1, 0)): mid_left,
    ((-1, 0), (0, -1), (0, 1), (1, 0)): mid_center,
    ((-1, 0), (0, -1), (0, 1)): mid_right,
    ((0, -1), (1, 0)): bottom_left,
    ((-1, 0), (0, -1), (1, 0)): bottom_center,
    ((-1, 0), (0, -1)): bottom_right,
}

# ------- OFFSETS ------- #
tile_offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]
NEARBY_OFFSET = [[-1, 0], [0, 0], [1, 0], [-1, -1],
                 [0, -1], [1, -1], [-1, 1], [0, 1], [1, 1]]
for p in [[[x - 2, y - 2] for x in range(5)] for y in range(5)]:
    NEARBY_OFFSET += p

HIT_TILE_PATH = 'src/images/tiles/tileset/'
OBJ_TILE_PATH = 'src/images/tiles/objects/'
'''
    Tile Map:
        - hash table
            - pos (x,y)
                - layers (-1,0,1)
                    - tiles [pos, tile_type, tile_name, image_id, pg.image]
                            [[8,8], tileset, tileset_0, 1, <Surface 16x16>]
'''


class TileMap:
    def __init__(self, app) -> None:
        self.app = app
        self.tiles = {}
        self.objects = {}
        self.all_layers = []

    def get_visible_tiles(self, surf, offset):
        layers = {l: [] for l in self.all_layers}
        objects = []
        for c in range(int(0 + offset[0] // s.CELL_SIZE) - 1, int((s.COLS * s.CELL_SIZE + offset[0]) // s.CELL_SIZE) + 2):
            for r in range(int(0 + offset[1] // s.CELL_SIZE) - 1, int((s.ROWS * s.CELL_SIZE + offset[1]) // s.CELL_SIZE) + 2):
                pos = (c, r)
                if pos in self.tile_map:
                    for layer, data in self.tile_map[pos].items():
                        tile_data = [pos] + data
                        layers[layer].append(tile_data)
                if pos in self.objects:
                    data = self.objects[pos]
                    tile = [pos] + data
                    objects.append(tile)
        return layers, objects

    def get_nearby_tiles(self, pos):
        p = [int(pos[0] // s.CELL_SIZE), int(pos[1] // s.CELL_SIZE)]
        tiles = []
        for offset in NEARBY_OFFSET:
            key = (p[0] + offset[0], p[1] + offset[1])
            if key in self.tile_map:
                for layer in self.tile_map[key]:
                    print(layer)
        return tiles

    def load_map(self, map):
        pass

# tile: (0,0): ['tileset', 'tileset_1', '0', 'src/tiles/tileset/tileset_1/0.png', <Surface(16x16x32 SW)>]
class Tile_Editor:
    def __init__(self, app) -> None:
        self.app = app
        self.tile_data = []
        self.tile_map = TileMap(self)
        self.layers = set()
        self.tiles = {}
        self.get_tile_data()

    def add_tile(self, pos, tile_data, layer):
        key = (int(pos[0]), int(pos[1]))
        if layer not in self.layers:
            self.layers.add(layer)
        if key not in self.tile_map.tiles:
            self.tile_map.tiles[key] = {}
            self.tile_map.tiles[key][layer] = tile_data
        self.tile_map.tiles[key][layer] = tile_data

    def remove_tile(self, pos, layer):
        key = (int(pos[0]), int(pos[1]))
        if key in self.tile_map.tiles:
            if layer in self.tile_map.tiles[key]:
                del self.tile_map.tiles[key][layer]
                if len(self.tile_map.tiles[key]) == 0:
                    del self.tile_map.tiles[key]

    def auto_tile(self, starting_pos, tileset_imgs, layer):
        v = set()
        key = tuple(starting_pos)
        if key not in self.tile_map.tiles:
            print('pos not in tile map')
            return
        if layer not in self.tile_map.tiles[key]:
            print('pos in tile map, but incorrect layer')
            return
        
        # ['tileset', 'tileset_1', '0', 'src/tiles/tileset/tileset_1/0.png', <Surface(16x16x32 SW)>]
        def dfs(pos, v: set):
            if pos in v:
                return
            v.add(pos)
            nearby_tiles = []
            neighbors = []
            for offset in tile_offsets:
                search_pos = (pos[0] + offset[0], pos[1] + offset[1])
                if search_pos in self.tile_map.tiles and layer in self.tile_map.tiles[search_pos]:
                    nearby_tiles.append(offset)
                    neighbors.append(search_pos)
            auto_tile_key = tuple(sorted(nearby_tiles))
            if auto_tile_key in auto_tile_config:
                tile_imgs = sorted(tileset_imgs)
                self.tile_map.tiles[pos][layer][-1] = utils.get_image(tile_imgs[auto_tile_config[auto_tile_key]], [s.CELL_SIZE,s.CELL_SIZE])
                self.tile_map.tiles[pos][layer][2] = str(auto_tile_config[auto_tile_key])
            for n in neighbors:
                dfs(n, v)
        dfs(key, v)


    def test_render(self, surf, offset=[0, 0]):
        for c in range(int(0 + offset[0] // s.CELL_SIZE) - 1, int((s.COLS * s.CELL_SIZE + offset[0]) // s.CELL_SIZE) + 2):
            for r in range(int(0 + offset[1] // s.CELL_SIZE) - 1, int((s.ROWS * s.CELL_SIZE + offset[1]) // s.CELL_SIZE) + 2):
                pos = (c, r)
                if pos in self.tile_map.tiles:
                    for layer, data in self.tile_map.tiles[pos].items():
                        surf.blit(data[-1], ( (pos[0] * s.CELL_SIZE) - offset[0], (pos[1] * s.CELL_SIZE) - offset[1]) )

    def get_visible_tiles(self, offset):
        layers = {l: [] for l in self.all_layers}
        objects = []
        for c in range(int(0 + offset[0] // s.CELL_SIZE) - 1, int((s.COLS * s.CELL_SIZE + offset[0]) // s.CELL_SIZE) + 2):
            for r in range(int(0 + offset[1] // s.CELL_SIZE) - 1, int((s.ROWS * s.CELL_SIZE + offset[1]) // s.CELL_SIZE) + 2):
                pos = (c, r)
                if pos in self.tile_map:
                    for layer, data in self.tile_map[pos].items():
                        tile_data = [pos] + data
                        layers[layer].append(tile_data)
                if pos in self.objects:
                    data = self.objects[pos]
                    tile = [pos] + data
                    objects.append(tile)
        return layers, objects

    def get_tile_data(self):
        # TILE_TYPES: tileset, bg_tiles, objects, markers
        # tileset are main tiles in game that entities cant get passed
        # bg_tiles are background tiles that arent meant to be interracted with NOTE: might be worth to cache it depending on size of bg
        # objects can have mutiple types with their own attributes
        # markere are spawn points for player, enemies, weapons, etc
        tileset_names = os.listdir(s.TILESET_PATH)
        bg_tile_names = os.listdir(s.BG_TILES_PATH)
        obj_names = os.listdir(s.OBJECTS_PATH)
        marker_names = os.listdir(s.MARKERS_PATH)
        decor_names = os.listdir(s.DECOR_PATH)

        # [tile_type:str, tile_name:str, images:list, config:dict]
        tilesets = []
        for tile_name in tileset_names:
            tile_ids = os.listdir(s.TILESET_PATH + f'{tile_name}')
            tile_ids.sort()
            tileset_images_paths = []
            config = None
            for tile_id in tile_ids:
                if tile_id[-3:] == 'png':
                    full_tileset_path = f'{s.TILESET_PATH}{tile_name}/{tile_id}'
                    tileset_images_paths.append(full_tileset_path)
                else:
                    f = open(f'{s.TILESET_PATH}{tile_name}/{tile_id}', 'r')
                    config = json.loads(f.read())
            tilesets.append(
                ['tileset', tile_name, tileset_images_paths, config])
        self.tile_data.append(tilesets)

        bg_tiles = []
        for bg_tile_name in bg_tile_names:
            bg_tile_ids = os.listdir(s.BG_TILES_PATH + f'{bg_tile_name}')
            bg_tile_ids.sort()
            bg_tiles_images_paths = []
            config = None
            for tile_id in bg_tile_ids:
                if tile_id[-3:] == 'png':
                    full_tileset_path = f'{s.BG_TILES_PATH}{bg_tile_name}/{tile_id}'
                    bg_tiles_images_paths.append(full_tileset_path)
                else:
                    f = open(f'{s.BG_TILES_PATH}{bg_tile_name}/{tile_id}', 'r')
                    config = json.loads(f.read())
            bg_tiles.append(['bg_tiles', bg_tile_name, bg_tiles_images_paths, config])
        self.tile_data.append(bg_tiles)

        decors = []
        for decor_name in decor_names:
            decor_ids = os.listdir(s.DECOR_PATH + f'{decor_name}')
            decor_ids.sort()
            decor_images_paths = []
            config = None
            for decor_id in decor_ids:
                if decor_id[-3:] == 'png':
                    full_decor_path = f'{s.DECOR_PATH}{decor_name}/{decor_id}'
                    decor_images_paths.append(full_decor_path)
                else:
                    f = open(f'{s.DECOR_PATH}{decor_name}/{decor_id}', 'r')
                    config = json.loads(f.read())
            decors.append(['decor', decor_name, decor_images_paths, config])
        self.tile_data.append(decors)


        '''
            [
                [
                    [tile_type:str, tile_name:str, images:list, config:dict],
                    [tile_type:str, tile_name:str, images:list, config:dict],
                ]
            ]
        '''
        
