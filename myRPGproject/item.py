import pygame
from settings import *

class Item(pygame.sprite.Sprite):
    def __init__(self, item_name: str, animation_player, groups: list, groups2: list, player, pos: tuple) -> None:
        super().__init__(groups)
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.pos = pos
        self.item_name = item_name
        self.image = pygame.image.load(item_data[self.item_name]['graphic']).convert_alpha()
        self.rect = self.image.get_rect(topleft = self.pos)
        self.animation_player = animation_player
        self.groups2 = groups2
        self.draw_item()

    def draw_item(self):
        self.display_surface.blit(self.image, self.pos)

    def use_item(self):
        if item_data[self.item_name]['type'] == 'hp':
            self.player.health += int((self.player.stats['health'] / 100) * item_data[self.item_name]['recovery'])
            if self.player.health > self.player.stats['health']:
                self.player.health = self.player.stats['health']
            self.animation_player.create_particles('aura', self.player.rect.center, self.groups2)
            
        
        if item_data[self.item_name]['type'] == 'mp':
            self.player.energy += int((self.player.stats['energy'] / 100) * item_data[self.item_name]['recovery'])
            if self.player.energy > self.player.stats['energy']:
                self.player.energy = self.player.stats['energy']
            self.animation_player.create_particles('aura', self.player.rect.center, self.groups2)

        self.del_img()

    def del_img(self):
        self.kill()

        