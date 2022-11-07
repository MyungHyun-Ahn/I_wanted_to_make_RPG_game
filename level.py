import pygame 
from settings import *
from tile import Tile
from player import Player
from debug import debug

# 수 많은 스프라이트를 효율적으로 관리할 수 있어야 함
class Level:
    def __init__(self) -> None:
        # 이미지 가져옴
        self.display_surface = pygame.display.get_surface()

        # 스프라이트 그룹 셋업
        self.visible_sprites = pygame.sprite.Group() # 스프라이트를 그리는 그룹
        self.obstacle_sprites = pygame.sprite.Group() # 플레이어가 충돌할 수 있는 스프라이트 그룹

        # 스프라이트 셋업
        self.create_map()
    
    # 맵을 그리는 메소드
    def create_map(self):
        # enumerate 함수 : 인덱스와 원소를 동시에 반복시킬 수 있게 함
        for row_index, row in enumerate(WORLD_MAP):
            # print(row) WORLD_MAP row 값을 출력
            # print(row_index) WORLD_MAP row 인덱스 값을 출력
            for col_index, col in enumerate(row):
                # 인덱스 * TILESIZE로 좌표를 계산
                x = col_index * TILESIZE
                y = row_index * TILESIZE

                if col == 'x':
                    # col이 x 일때 돌을 그림
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                
                if col == 'p':
                    # col이 p 일때 플레이어를 그림
                    self.player = Player((x,y),[self.visible_sprites], self.obstacle_sprites)
    
    def run(self):
        # update and draw the game
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()
        debug(self.player.direction)