import pygame 
from settings import *
from tile import Tile
from player import Player

class Level:
    def __init__(self) -> None:
        # 이미지 가져옴
        self.display_surface = pygame.display.get_surface()

        # 스프라이트 그룹 셋업
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        # 스프라이트 셋업
        
    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE

                if col == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                
                if col == 'p':
                    Player((x,y),[self.visible_sprites])
    
    def run(self):
        # update and draw the game
        self.visible_sprites.draw(self.display_surface)