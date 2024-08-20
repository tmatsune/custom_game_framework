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

class TileMap:
    def __init__(self, app) -> None:
        self.app = app 
        self.tiles = {}
        self.objects = {}
    