import pygame
from settings import *
from support import import_folder
from debug import debug
from typing import Callable

# pygame Sprite 클래스 상속
class Player(pygame.sprite.Sprite):
    # 생성자
    def __init__(self, pos: tuple, groups: list, obstacle_sprites: pygame.sprite.Group, create_attack: Callable, destroy_attack: Callable) -> None:
        # 부모 클래스의 생성자를 먼저 로드
        super().__init__(groups)
        # .convert_alpha() : blit의 속도를 향상시킴
        # 픽셀당 알파를 포함하여 이미지의 픽셀 형식 변경
        self.image = pygame.image.load('resource/graphics/test/player.png').convert_alpha()
        # .get_rect 이미지의 직사각형 영역을 가져옴
        self.rect = self.image.get_rect(topleft = pos)
        # 플레이어의 전체 이미지 테두리 / 충돌 처리시 hitbox로 처리
        self.hitbox = self.rect.inflate(0, -26)

        # 그래픽 세팅
        self.import_player_assets()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15

        # 벡터
        # default [ x : 0 -> 1 * speed (이동속도) ] 
        #         [ y : 0 -> 1 * speed (이동속도) ]
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        # 장애물 받아오기
        self.obstacle_sprites = obstacle_sprites

		# weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None 
        self.switch_duration_cooldown = 200

    def import_player_assets(self):
        charater_path = 'resource/graphics/player/'
        self.animations = {
            'up'           : [],
            'down'         : [],
            'left'         : [],
            'right'        : [],
			'right_idle'   : [],
            'left_idle'    : [],
            'up_idle'      : [],
            'down_idle'    : [],
			'right_attack' : [],
            'left_attack'  : [],
            'up_attack'    : [],
            'down_attack'  : []
        }
        
        for animation in self.animations.keys():
            full_path = charater_path + animation
            self.animations[animation] = import_folder(full_path)

    # 키보드 입력 받기
    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            # attack input
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
            
            # magic input
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()

            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()

                if self.weapon_index < len(list(weapon_data.keys())) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0

                self.weapon = list(weapon_data.keys())[self.weapon_index]

    def get_status(self):
        # idle status
        debug("status : {}".format(self.status), x=250, y=10)
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'
        
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

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

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True
    
    def animate(self):
        animation = self.animations[self.status]

		# loop over the frame index 
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

		# set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)