import pygame as pg, os, json
import src.settings as set 
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
tile_offsets = [ (1, 0), (-1, 0), (0, 1), (0, -1) ]
NEARBY_OFFSET = [[-1, 0], [0, 0], [1, 0],[-1, -1], [0, -1], [1, -1], [-1, 1], [0, 1], [1, 1]]
for p in [[[x - 2, y - 2] for x in range(5)] for y in range(5)]: NEARBY_OFFSET += p

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
        for c in range(int(0 + offset[0] // set.CELL_SIZE) - 1, int((set.COLS*set.CELL_SIZE + offset[0]) // set.CELL_SIZE) + 2):
            for r in range(int(0 + offset[1] // set.CELL_SIZE) - 1, int((set.ROWS*set.CELL_SIZE + offset[1]) // set.CELL_SIZE) + 2):
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
        p = [int(pos[0] // set.CELL_SIZE), int(pos[1] // set.CELL_SIZE)]
        tiles = []
        for offset in NEARBY_OFFSET:
            key = (p[0] + offset[0], p[1] + offset[1])
            if key in self.tile_map:
                for layer in self.tile_map[key]:
                    print(layer)
        return tiles
    
    def load_map(self, map):
        pass


class Tile_Editor:
    def __init__(self, app) -> None:
        self.app = app
        self.tile_data = []
        self.tile_map = TileMap(self)
        self.layers = {}
        self.get_tile_data()

    def get_tile_data(self):
        # TILE_TYPES: tileset, bg_tiles, objects, markers
        # tileset are main tiles in game that entities cant get passed 
        # bg_tiles are background tiles that arent meant to be interracted with NOTE: might be worth to cache it depending on size of bg 
        # objects can have mutiple types with their own attributes
        # markere are spawn points for player, enemies, weapons, etc 
        tileset_names = os.listdir(set.TILESET_PATH)
        bg_tile_names = os.listdir(set.BG_TILES_PATH)
        obj_names = os.listdir(set.OBJECTS_PATH)
        marker_names = os.listdir(set.MARKERS_PATH)
        decor_names = os.listdir(set.DECOR_PATH)

        # [tile_type, tile_name, images, config]
        tilesets = []
        for tile_name in tileset_names:
            tile_ids = os.listdir(set.TILESET_PATH+f'{tile_name}')
            tile_ids.reverse()
            tileset_images_paths = []
            config = None
            for tile_id in tile_ids:
                if tile_id[-3:] == 'png':
                    full_tileset_path = f'{set.TILESET_PATH}{tile_name}/{tile_id}'
                    tileset_images_paths.append(full_tileset_path)
                else:
                    f = open(f'{set.TILESET_PATH}{tile_name}/{tile_id}', 'r')
                    config = json.loads(f.read())
            tilesets.append(['tileset', tile_name, tileset_images_paths, config])
            
            
        
