import pygame, sys
from settings import *
from level import Level
from debug import debug
import time

class Game:
    def __init__(self) -> None:
        # 게임 기본 세팅
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))

        # 타이틀 설정
        pygame.display.set_caption('RPG 게임을 만들고 싶었다')
        self.background_music = pygame.mixer.Sound('resource/audio/background/main.ogg')

        # FPS 설정을 위한 Clock 객체
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        # 배경음악 무한 재생
        self.background_music.play(-1)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.level.toggle_menu()

            self.screen.fill('black')
            self.level.run()
            if self.level.check_game_over():
                show_restart_menu("GAME OVER")
            pygame.display.update()
            self.clock.tick(FPS)


def main():
    game = Game()
    game.run()    

# if __name__ == '__main__':
# 	game = Game()
# 	game.run()

import pygame_menu

screen = pygame.display.set_mode((WIDTH, HEIGTH))

def start_the_game():
    main()

def show_start_menu():
    hanfont = pygame.font.SysFont("malgungothic", 30)
    t = pygame_menu.themes.THEME_BLUE.copy()
    t.widget_font=hanfont
    menu = pygame_menu.Menu("Menu", WIDTH, HEIGTH, theme=t)
    menu.add.button("게임 시작", start_the_game)
    menu.add.button("게임 종료", pygame_menu.events.EXIT)
    menu.mainloop(screen)

def show_restart_menu(message):
    hanfont = pygame.font.SysFont("malgungothic", 30)
    t = pygame_menu.themes.THEME_BLUE.copy()
    t.widget_font=hanfont
    menu = pygame_menu.Menu("Menu", 500, 300,theme=t)
    menu.add.button("다시 하기", show_start_menu)
    menu.add.button("게임 종료", pygame_menu.events.EXIT)
    menu.mainloop(screen)

if __name__ == '__main__':
    show_start_menu()
