import pygame
from settings import *

# pygame Sprite 클래스 상속
class Player(pygame.sprite.Sprite):
    # 생성자
    def __init__(self, pos, groups) -> None:
        # 부모 클래스의 생성자를 먼저 로드
        super().__init__(groups)
        
        # .convert_alpha() : blit의 속도를 향상시킴
        # 픽셀당 알파를 포함하여 이미지의 픽셀 형식 변경
        self.image = pygame.image.load('resource/graphics/test/player.png').convert_alpha()

        # .get_rect 이미지의 직사각형 영역을 가져옴
        self.rect = self.image.get_rect(topleft = pos)