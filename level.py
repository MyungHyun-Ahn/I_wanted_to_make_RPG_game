import pygame 
from pygame.locals import Rect
from settings import *
from tile import Tile
from item import Item
from player import Player
from debug import debug
from support import * 
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade


class Level:
	def __init__(self, difficulty, restart_game):
		# 이미지 가져옴
		self.display_surface = pygame.display.get_surface()
		self.game_paused = False

		# 스프라이트 그룹 셋업
		# self.visible_sprites = pygame.sprite.Group() # 스프라이트를 그리는 그룹
		self.visible_sprites = YSortCameraGroup() # 커스텀 그룹
		self.obstacle_sprites = pygame.sprite.Group() # 플레이어가 충돌할 수 있는 스프라이트 그룹
		self.item_sprites = pygame.sprite.Group()

		# 공격 스프라이트
		self.current_attack = None
		self.attack_sprites = pygame.sprite.Group()
		self.attackable_sprites = pygame.sprite.Group()

		# map option 초기값
		self.map_size = MAPSIZE
		self.grass_count = GRASSCOUNT
		self.object_count = OBJECTCOUNT
		self.entity_count = ENTITYCOUNT

		self.monster_count = self.entity_count

		# 난이도 설정
		self.game_difficulty = difficulty

		# round
		self.round = 0

		# ticks
		self.round_ticks = 0
		self.end_ticks = 0
		self.game_over_ticks = 0

		# game over
		self.game_over = False

		# 스프라이트 셋업
		self.create_map()

		# user interface
		self.ui = UI()
		self.upgrade = Upgrade(self.player)

		# particles
		self.animation_player = AnimationPlayer()
		self.magic_player = MagicPlayer(self.animation_player)

		self.restart_game = restart_game
		# game over sound
		self.game_over_sound = pygame.mixer.Sound('resource/audio/GameOver2.wav')

	def create_map(self):
		self.round += 1
		self.round_ticks = 0

		self.map_upgrade()
		self.reset_map()
		
		# 스프라이트 그룹을 초기화
		self.visible_sprites.empty()
		self.obstacle_sprites.empty()
		self.item_sprites.empty()
		self.attack_sprites.empty()
		self.attackable_sprites.empty()
		

		boundary = import_csv_layout('resource/map/boundary.csv')
		grass = import_csv_layout('resource/map/grass.csv')
		objectl = import_csv_layout('resource/map/object.csv')
		entities = import_csv_layout('resource/map/entities.csv')

		layouts = {
			'boundary': boundary,
			'grass': grass,
			'object': objectl,
			'entities' : entities
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
							if col == 'r': # r : rock
								rock_image = pygame.image.load('resource/graphics/test/rock.png').convert_alpha()
								Tile(
									(x, y),
									[self.visible_sprites, self.obstacle_sprites],
									'rock',
									rock_image
								)
								
							if col == 'p':
								if self.round == 1:
									self.player = Player(
										(x, y),
										self.map_size,
										[self.visible_sprites],
										self.obstacle_sprites,
										self.item_sprites,
										self.create_attack,
										self.destroy_attack,
										self.create_magic
									)
								else:
									self.player.goto_xy((x, y), [self.visible_sprites])
									self.player.set_map_size(self.map_size)

							if col == 'o':
								surf = graphics['objects'][21]
								Tile(
									(x, y),
									[self.visible_sprites],
									'portal',
									surf
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
							if col == 'm':
								monster_name = choice(normal_monster_name)
								monster_type = 'normal'
								
							Enemy(
								monster_name, 
								monster_type,
								self.game_difficulty,
								self.round,
								self.map_size,
								(x, y), 
								[self.visible_sprites, self.attackable_sprites], 
								self.obstacle_sprites,
								self.damage_player,
								self.trigger_death_particles,
								self.monster_count_down,
								self.drop_item,
								self.add_exp,
								self.drop_weapon
							)

	def map_upgrade(self):
		self.map_size = MAPSIZE + (self.round // 5) * 5 # 5라운드마다 map_size 5 씩 증가
		self.grass_count = GRASSCOUNT + (self.round // 5) * 5 # 5라운드마다 grass 5 씩 증가
		self.object_count = OBJECTCOUNT + (self.round // 10) * 5 # 10라운드마다 오브젝트 5개씩 증가
		self.entity_count = ENTITYCOUNT + (self.round // 3) * 2 # 3라운드마다 몬스터 3마리씩 증가


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

		if style == 'p_leaf_attack':
			self.magic_player.leaf_attack(self.player, cost, [self.visible_sprites, self.attack_sprites])

		if style == 'p_thunder':
			self.magic_player.thunder(self.player, cost, [self.visible_sprites, self.attack_sprites])


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

	def add_exp(self, amount):
		self.player.exp += amount

	def toggle_menu(self):
		self.game_paused = not self.game_paused

	# setter
	def monster_count_down(self):
		self.monster_count -= 1

	
	def display_round(self):
		if self.round_ticks < 120:
			self.ui.draw_round(self.round)
			self.round_ticks += 1

	def reset_map(self):
		# self.visible_sprites = YSortCameraGroup() # 커스텀 그룹
		# self.obstacle_sprites = pygame.sprite.Group() # 플레이어가 충돌할 수 있는 스프라이트 그룹

		boundary_list = make_boundary_list(self.map_size)
		list_to_csv(boundary_list, 'boundary')
		grass_list = make_grass_list(self.map_size, self.grass_count, boundary_list)
		list_to_csv(grass_list, 'grass')
		object_list = make_object_list(self.map_size, range(19), self.object_count, boundary_list, grass_list)
		list_to_csv(object_list, 'object')
		entity_list = make_entity_list(self.map_size, self.entity_count, boundary_list, grass_list, object_list)
		list_to_csv(entity_list, 'entities')	
		self.monster_count = self.entity_count
		print("맵 생성 완료")
		
	def check_remain_monster(self):
		return self.monster_count

	def update_stage(self):
		if self.check_remain_monster() == 0:
			self.round_ticks += 1
			self.ui.draw_clear(6 - int(self.round_ticks / 60))
			if self.round_ticks > 380:
				self.create_map()
				self.spawn_boss()

	def get_player(self):
		return self.player

	def drop_item(self, pos: tuple):
		"""
		아이템 드롭률
		LifePot : 30%
		Medipack : 10%
		WaterPot : 20%
		"""
		rate = randint(0, 100)

		if rate < 30:
			Item('waterpot', 'item', animation_player = self.animation_player, groups = [self.visible_sprites, self.item_sprites], groups2 = [self.visible_sprites], player = self.player, pos = pos)
		elif rate < 40:
			Item('medipack', 'item', animation_player = self.animation_player, groups = [self.visible_sprites, self.item_sprites], groups2 = [self.visible_sprites], player = self.player, pos = pos)
		elif rate < 60:
			Item('lifepot', 'item', animation_player = self.animation_player, groups = [self.visible_sprites, self.item_sprites], groups2 = [self.visible_sprites], player = self.player, pos = pos)
		else:
			pass

	def drop_weapon(self, pos: tuple):
		"""
		보스 처치시 무기 드롭
		획득시 자동 변경
		"""
		weapon_index = choice(range(len(weapon_data.keys())))
		print(weapon_index)
		Item(weapon_index, 'weapon', groups = [self.visible_sprites, self.item_sprites], player = self.player, pos = pos)


		
	
	def spawn_boss(self):
		if self.round % 10 == 0: # 10라운드마다 보스 2마리 소환
			monster_name1 = choice(boss_monster_name)
			monster_name2 = choice(boss_monster_name)
			Enemy(
				monster_name1, 
				"unique",
				self.game_difficulty,
				self.round,
				self.map_size,
				(((self.map_size - 1) // 2) * TILESIZE - 100, ((self.map_size - 1) // 2) * TILESIZE), 
				[self.visible_sprites, self.attackable_sprites], 
				self.obstacle_sprites,
				self.damage_player,
				self.trigger_death_particles,
				self.monster_count_down,
				self.drop_item,
				self.add_exp,
				self.drop_weapon
			)
			Enemy(
				monster_name2, 
				"unique",
				self.game_difficulty,
				self.round,
				self.map_size,
				(((self.map_size - 1) // 2) * TILESIZE + 100, ((self.map_size - 1) // 2) * TILESIZE), 
				[self.visible_sprites, self.attackable_sprites], 
				self.obstacle_sprites,
				self.damage_player,
				self.trigger_death_particles,
				self.monster_count_down,
				self.drop_item,
				self.add_exp,
				self.drop_weapon
			)
			self.monster_count += 2
		elif self.round % 1 == 0:
			monster_name = choice(boss_monster_name)
			print(monster_name)
			Enemy(
				monster_name, 
				"unique",
				self.game_difficulty,
				self.round,
				self.map_size,
				(((self.map_size - 1) // 2) * TILESIZE, ((self.map_size - 1) // 2) * TILESIZE), 
				[self.visible_sprites, self.attackable_sprites], 
				self.obstacle_sprites,
				self.damage_player,
				self.trigger_death_particles,
				self.monster_count_down,
				self.drop_item,
				self.add_exp,
				self.drop_weapon
			)
			self.monster_count += 1
		print((((self.map_size - 1) // 2) * TILESIZE, ((self.map_size - 1) // 2) * TILESIZE))

	def check_game_over(self):
		if self.player.health <= 0:
			self.game_over_ticks += 1
			if self.game_over_ticks > 150:
				self.restart_game("GAME_OVER")
				




	def run(self):
		# 배경 그리기
		# self.visible_sprites.draw(self.display_surface)
		# self.draw_background()
		self.visible_sprites.custom_draw(self.player, self.map_size)
		self.ui.display(self.player, self.monster_count)

		if self.game_paused:
			self.upgrade.display()
		else:
			self.visible_sprites.update()
			self.visible_sprites.enemy_update(self.player)
			self.player_attack_logic()	
		
		self.display_round()
		if self.player.health <= 0:
			# self.ui.draw_game_over()
			self.game_over_sound.play(2)
		# self.check_game_over()
		self.update_stage()
		


# Y좌표 기준으로 카메라를 정렬
class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self):
		# general setup 
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		self.offset = pygame.math.Vector2()
		self.offset2 = pygame.math.Vector2()
		self.background_img = pygame.image.load("resource/map/test.png")
		self.background_rect = self.background_img.get_rect()

	def custom_draw(self,player, mapsize):
		# getting the offset 
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height
		
		back_offset_pos = self.background_rect.topleft - self.offset
		# 배경그리기
		self.display_surface.blit(self.background_img, back_offset_pos, Rect(0, 0, mapsize * TILESIZE, mapsize * TILESIZE))

		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image,offset_pos)

	def enemy_update(self, player: Player):
		enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
		for enemy in enemy_sprites:
			self.offset2.x = player.rect.centerx - self.half_width
			self.offset2.y = player.rect.centery - self.half_height
			offset_pos = enemy.rect.topleft - self.offset2
			enemy.enemy_update(player, offset_pos)