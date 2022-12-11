import pygame
from settings import *
from support import import_folder
from debug import debug
from entity import Entity
from typing import Callable
from item import Item
from random import randint
# pygame Sprite 클래스 상속
class Player(Entity):
    # 생성자
    def __init__(self, pos: tuple, map_size: int, groups: list, obstacle_sprites: pygame.sprite.Group, item_sprites: pygame.sprite.Group, create_attack: Callable, destroy_attack: Callable, create_magic: Callable) -> None:
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
        # self.frame_index = 0
        # self.animation_speed = 0.15

        # 벡터
        # default [ x : 0 -> 1 * speed (이동속도) ] 
        #         [ y : 0 -> 1 * speed (이동속도) ]
        # movement
        # self.direction = pygame.math.Vector2()
        # self.speed = 5
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        # 장애물 받아오기
        self.obstacle_sprites = obstacle_sprites

        # item
        self.item_sprites = item_sprites

		# weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]

        # magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[0]

        # stats
        self.stats = {
            'health' : 100,
            'energy' : 60,
            'attack' : 10,
            'magic'  : 5,
            'speed'  : 8
        }

        self.max_stats = {
            'health' : 99999,
            'energy' : 99999,
            'attack' : 500000,
            'magic'  : 500000,
            'speed'  : 300
        }

        self.upgrade_rate = {
            'health' : 10,
            'energy' : 10,
            'attack' : 5,
            'magic'  : 5,
            'speed'  : 3
        }

        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.speed  = self.stats['speed']
        self.level = 1
        self.exp    = 0
        self.level_up_exp = 500
        self.stat_point = 0

        # damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

        self.map_size = map_size

        # import a sound
        self.weapon_attack_sound = pygame.mixer.Sound('resource/audio/sword.wav')
        self.weapon_attack_sound.set_volume(0.4)

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
            if keys[pygame.K_a]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                self.weapon_attack_sound.play()
            
            # magic input
            if keys[pygame.K_q]:
                self.magic = list(magic_data.keys())[0]
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[0]
                strength = list(magic_data.values())[0]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[0]['cost']
                self.create_magic(style, strength, cost)

            if keys[pygame.K_w]:
                self.magic = list(magic_data.keys())[1]
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[1]
                strength = list(magic_data.values())[1]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[1]['cost']
                self.create_magic(style, strength, cost)
            
            if keys[pygame.K_e]:
                self.magic = list(magic_data.keys())[2]
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[2]
                strength = list(magic_data.values())[2]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[2]['cost']
                self.create_magic(style, strength, cost)

            if keys[pygame.K_r]:
                self.magic = list(magic_data.keys())[3]
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[3]
                strength = list(magic_data.values())[3]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[3]['cost']
                self.create_magic(style, strength, cost)
        

    def get_status(self):
        # idle status
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

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.item('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.item('vertical')
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

    def item(self, direction: pygame.math.Vector2) -> None:
        for item in self.item_sprites:
            if direction == 'horizontal':
                if item.rect.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        item.use_item()
                    if self.direction.y < 0:
                        item.use_item()

        for item in self.item_sprites:
            if direction == 'vertical':
                if item.rect.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        item.use_item()
                    if self.direction.y < 0:
                        item.use_item()
    
    def change_weapon(self, weapon_index):
        self.weapon = list(weapon_data.keys())[weapon_index]

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True
    
    def animate(self):
        animation = self.animations[self.status]

		# loop over the frame index 
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

		# set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        # flicker
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage

    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        spell_damage = magic_data[self.magic]['strength']
        return base_damage + spell_damage

    def get_value_by_index(self, index):
        return list(self.stats.values())[index]


    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            self.energy += 0.05 * self.stats['magic']
        else:
            self.energy = self.stats['energy']
    
    def goto_xy(self, xy: tuple, groups: list):
        super().__init__(groups)
        self.hitbox.x = xy[0]
        self.hitbox.y = xy[1]

    
    def set_map_size(self, map_size: int) -> None:
        self.map_size = map_size

    def level_up(self):
        if self.exp >= self.level_up_exp:
            self.exp -= self.level_up_exp
            self.level_up_exp *= 1.1
            self.level_up_exp = int(self.level_up_exp)
            self.stat_point += 3
            self.level += 1

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.out_map()
        self.level_up()
        self.move(self.speed)
        self.energy_recovery()