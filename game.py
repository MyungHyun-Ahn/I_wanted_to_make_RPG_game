import pygame, sys
from datafile import *
from pygame.locals import *

clock = pygame.time.Clock()

pygame.init()

WINDOW_SIZE = (640, 480)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
pygame.display.set_caption('RPG tutorial')

spr_character = SpriteSheet('spriteSheet1.png', 16, 16, 8, 8, 11)

while True:
    screen.blit(spr_character.spr[0], (320, 240))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    pygame.display.update()
    clock.tick(60)
