import pygame
from math import sin
from random import randint
from settings import *

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups: list) -> None:
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()

    def move(self, speed: float):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center
    
    def collision(self, direction: str):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: 
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def out_map(self):
        x_pos = randint(TILESIZE, (self.map_size - 2) * TILESIZE)
        y_pos = randint(TILESIZE, (self.map_size - 2) * TILESIZE)

        if self.hitbox.x < 0 or self.hitbox.y < 0:
            self.hitbox.x = x_pos
            self.hitbox.y = y_pos
        elif self.hitbox.x < 0 or self.hitbox.y > (self.map_size - 1) * TILESIZE:
            self.hitbox.x = x_pos
            self.hitbox.y = y_pos
        elif self.hitbox.x > (self.map_size - 1) * TILESIZE or self.hitbox.y < 0:
            self.hitbox.x = x_pos
            self.hitbox.y = y_pos
        elif self.hitbox.x > (self.map_size - 1) * TILESIZE or self.hitbox.y > (self.map_size - 1)  * TILESIZE:
            self.hitbox.x = x_pos
            self.hitbox.y = y_pos

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0