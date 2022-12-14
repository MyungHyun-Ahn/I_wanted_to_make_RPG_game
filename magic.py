import pygame
from settings import *
from random import randint

class MagicPlayer:
    def __init__(self, animation_player) -> None:
        self.animation_player = animation_player
        self.sounds = {
            'heal'  : pygame.mixer.Sound('resource/audio/heal.wav'),
		    'flame' : pygame.mixer.Sound('resource/audio/Fire.wav')
        }
    
    def heal(self, player, strength, cost, groups):
        if player.energy >= cost:
            self.sounds['heal'].play()
            player.health += strength
            player.energy -= cost
            if player.health >= player.stats['health']:
                player.health = player.stats['health']
            self.animation_player.create_particles('aura', player.rect.center, groups)
            self.animation_player.create_particles('heal', player.rect.center, groups)

    def flame(self, player, cost, groups):
        if player.energy >= cost:
            self.sounds['flame'].play()
            player.energy -= cost
            
            if player.status.split('_')[0] == 'right':
                direction = pygame.math.Vector2(1, 0)
            elif player.status.split('_')[0] == 'left':
                direction = pygame.math.Vector2(-1, 0)
            elif player.status.split('_')[0] == 'up':
                direction = pygame.math.Vector2(0, -1)
            else:
                direction = pygame.math.Vector2(0, 1)
            
            for i in range(1, 6):
                if direction.x:
                    offset_x = (direction.x * i) * TILESIZE
                    x = player.rect.centerx + offset_x + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles('flame', (x, y), groups)
                else:
                    offset_y = (direction.y * i) * TILESIZE
                    x = player.rect.centerx + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + offset_y + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles('flame',(x, y), groups)

    def leaf_attack(self, player, cost, groups):
        if player.energy >= cost:
            player.energy -= cost

            if player.status.split('_')[0] == 'right':
                direction = pygame.math.Vector2(1, 0)
            elif player.status.split('_')[0] == 'left':
                direction = pygame.math.Vector2(-1, 0)
            elif player.status.split('_')[0] == 'up':
                direction = pygame.math.Vector2(0, -1)
            else:
                direction = pygame.math.Vector2(0, 1)

            if direction.x:
                offset_x = direction.x * TILESIZE
                x = player.rect.centerx + offset_x
                y = player.rect.centery
                self.animation_player.create_particles('p_leaf_attack', (x, y), groups)
            else:
                offset_y = direction.y * TILESIZE
                x = player.rect.centerx
                y = player.rect.centery + offset_y
                self.animation_player.create_particles('p_leaf_attack', (x, y), groups)

    def thunder(self, player, cost, groups):
        if player.energy >= cost:
            player.energy -= cost

            if player.status.split('_')[0] == 'right':
                direction = pygame.math.Vector2(1, 0)
            elif player.status.split('_')[0] == 'left':
                direction = pygame.math.Vector2(-1, 0)
            elif player.status.split('_')[0] == 'up':
                direction = pygame.math.Vector2(0, -1)
            else:
                direction = pygame.math.Vector2(0, 1)
            
            for i in range(1, 4):
                if direction.x:
                    offset_x = (direction.x * i * 2) * TILESIZE
                    x = player.rect.centerx + offset_x + randint(-TILESIZE, TILESIZE)
                    y = player.rect.centery + randint(-TILESIZE, TILESIZE)
                    self.animation_player.create_particles('p_thunder', (x, y), groups)
                else:
                    offset_y = (direction.y * i * 2) * TILESIZE
                    x = player.rect.centerx + randint(-TILESIZE, TILESIZE)
                    y = player.rect.centery + offset_y + randint(-TILESIZE, TILESIZE)
                    self.animation_player.create_particles('p_thunder',(x, y), groups)

        

            