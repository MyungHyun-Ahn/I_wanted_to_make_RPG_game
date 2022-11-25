import pygame 
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import * 
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer
# 수 많은 스프라이트를 효율적으로 관리할 수 있어야 함
class Level:
    def __init__(self) -> None:
        # 이미지 가져옴
        self.display_surface = pygame.display.get_surface()

        # 스프라이트 그룹 셋업
        # self.visible_sprites = pygame.sprite.Group() # 스프라이트를 그리는 그룹
        self.visible_sprites = YSortCameraGroup() # 커스텀 그룹
        self.obstacle_sprites = pygame.sprite.Group() # 플레이어가 충돌할 수 있는 스프라이트 그룹

        # 공격 스프라이트
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # 스프라이트 셋업
        self.create_map()

        # user interface
        self.ui = UI()

        # particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)
    
    # # 맵을 그리는 메소드
    # def create_map(self):
    #     # enumerate 함수 : 인덱스와 원소를 동시에 반복시킬 수 있게 함
    #     for row_index, row in enumerate(WORLD_MAP):
    #         # print(row) WORLD_MAP row 값을 출력
    #         # print(row_index) WORLD_MAP row 인덱스 값을 출력
    #         for col_index, col in enumerate(row):
    #             # 인덱스 * TILESIZE로 좌표를 계산
    #             x = col_index * TILESIZE
    #             y = row_index * TILESIZE

    #             if col == 'x':
    #                 # col이 x 일때 돌을 그림
    #                 Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                
    #             if col == 'p':
    #                 # col이 p 일때 플레이어를 그림
    #                 self.player = Player((x,y),[self.visible_sprites], self.obstacle_sprites)
    
    def create_map(self):
        layouts = {
			'boundary': import_csv_layout('resource/map/map_FloorBlocks.csv'),
			'grass': import_csv_layout('resource/map/map_Grass.csv'),
			'object': import_csv_layout('resource/map/map_Objects.csv'),
            'entities' : import_csv_layout('resource/map/map_Entities.csv')
		}
        graphics = {
			'grass': import_folder('resource/graphics/Grass'),
			'objects': import_folder('resource/graphics/objects')
		}

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile(
                                (x, y), 
                                [self.obstacle_sprites],
                                'invisible'
                            )

                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile(
                                (x, y), 
                                [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites], 
                                'grass', 
                                random_grass_image
                            )

                        if style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile(
                                (x, y), 
                                [self.visible_sprites, self.obstacle_sprites], 
                                'object', 
                                surf
                            )

                        if style == 'entities':
                            if col == '394':
                                self.player = Player(
                                    (x, y),
                                    [self.visible_sprites],
                                    self.obstacle_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic
                                )
                            else:
                                if col == '390':
                                    monster_name = 'bamboo'
                                elif col == '391':
                                    monster_name = 'spirit'
                                elif col == '392':
                                    monster_name = 'raccoon'
                                else:
                                    monster_name = 'squid'
                                Enemy(
                                    monster_name, 
                                    (x, y), 
                                    [self.visible_sprites, self.attackable_sprites], 
                                    self.obstacle_sprites,
                                    self.damage_player,
                                    self.trigger_death_particles
                                )
                        
    def create_attack(self):
        self.current_attack = Weapon(
            self.player, 
            [self.visible_sprites, self.attack_sprites]
        )

    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])

        if style == 'flame':
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            print("weapon kill")
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 75)
                            for leaf in range(randint(3, 6)):
                                self.animation_player.create_grass_particles(pos - offset, [self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos, self.visible_sprites)

    def run(self):
        # 배경 그리기
        # self.visible_sprites.draw(self.display_surface)

        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.ui.display(self.player)


# Y좌표 기준으로 카메라를 정렬
class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # 화면의 중간 구하기
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2

        # 카메라의 왼쪽 위 좌표를 담는 벡터
        self.offset = pygame.math.Vector2()


        self.floor_surf = pygame.image.load('resource/graphics/tilemap/ground.png').convert_alpha()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0, 0))

    # player의 좌표 정보를 받아 카메라 위치 계산
    def custom_draw(self, player: Player):
        # 좌표 받아오기
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # for sprite in self.sprites():
        #     offset_pos = sprite.rect.topleft + self.offset
        #     self.display_surface.blit(sprite.image, offset_pos)

        # for sprite in self.sprites():
        # self.sprites()를 y값 기준으로 정렬 / 이미지 출력 순서 정렬
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player: Player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)


