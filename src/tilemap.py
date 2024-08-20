import pygame as pg 

class TileMap:
    def __init__(self, app) -> None:
        self.app = app 
        self.tiles = {}
        