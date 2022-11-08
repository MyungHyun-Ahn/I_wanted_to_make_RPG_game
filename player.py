import pygame
from settings import *

# pygame Sprite 클래스 상속
class Player(pygame.sprite.Sprite):
    # 생성자
    def __init__(self, pos: tuple, groups: list, obstacle_sprites: pygame.sprite.Group()) -> None:
        # 부모 클래스의 생성자를 먼저 로드
        super().__init__(groups)
        
        # .convert_alpha() : blit의 속도를 향상시킴
        # 픽셀당 알파를 포함하여 이미지의 픽셀 형식 변경
        self.image = pygame.image.load('resource/graphics/test/player.png').convert_alpha()

        # .get_rect 이미지의 직사각형 영역을 가져옴
        self.rect = self.image.get_rect(topleft = pos)

        self.hitbox = self.rect.inflate(0, -26)
        # 벡터
        # default [ x : 0 -> 1 * speed (이동속도) ] 
        #         [ y : 0 -> 1 * speed (이동속도) ]
        self.direction = pygame.math.Vector2()

        self.speed = 20

        # 장애물 받아오기
        self.obstacle_sprites = obstacle_sprites

    # 키보드 입력 받기
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def move(self, speed: int) -> None:
        if self.direction.magnitude() != 0: # magitude : 벡터의 크기
            self.direction = self.direction.normalize()

            # self.direction += self.direction.x * speed
            # self.collision('horizontal')
            # self.rect.y += self.direction.y * speed
            # self.collision('vertical')
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        # self.rect.center += self.direction * speed # 정규화가 필요함, 벡터의 길이를 1로 만드는 것
        self.rect.center = self.hitbox.center

    def collision(self, direction: pygame.math.Vector2) -> None:
        # 수평 : 좌우로 걸을 때
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: # 오른쪽 이동
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: # 왼쪽 이동
                        self.hitbox.left = sprite.hitbox.right
        
        # 수직 : 위아래로 걸을 때
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: # 아래로 이동
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def update(self):
        self.input()
        self.move(self.speed)