import pygame, sys
from settings import *
from level import Level
from debug import debug

class Game:
    def __init__(self) -> None:
        # 게임 기본 세팅
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))

        # 타이틀 설정
        pygame.display.set_caption('RPG 게임을 만들고 싶었다')

        # FPS 설정을 위한 Clock 객체
        self.clock = pygame.time.Clock()
        self.level = Level(game_difficulty, show_restart_menu)

    def run(self):
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
background_music = pygame.mixer.Sound('resource/audio/background/main.ogg')
background_music.set_volume(0.5)
game_difficulty = 1

def set_difficulty(value, difficulty):
    global game_difficulty
    if difficulty == 1 :
        game_difficulty = 0.5
    elif difficulty == 2 :
        game_difficulty = 1
    else :
        game_difficulty = 2

def start_the_game():
    main()

def show_start_menu():
    hanfont = pygame.font.SysFont("malgungothic", 30)
    t = pygame_menu.themes.THEME_BLUE.copy()
    t.widget_font = hanfont
    menu = pygame_menu.Menu("GAME MENU", WIDTH, HEIGTH, theme=t)
    menu.add.selector("난이도", [("EASY", 1),("NORMAL", 2),("HARD", 3)],
                      onchange=set_difficulty)
    menu.add.button("게임 시작", start_the_game)
    menu.add.button("게임 종료", pygame_menu.events.EXIT)
    menu.mainloop(screen)

def show_restart_menu(message):
    hanfont = pygame.font.SysFont("malgungothic", 30)
    t = pygame_menu.themes.THEME_BLUE.copy()
    t.widget_font = hanfont
    menu = pygame_menu.Menu("GAME OVER", 500, 300,theme=t)
    menu.add.button("다시 하기", show_start_menu)
    menu.add.button("게임 종료", pygame_menu.events.EXIT)
    menu.mainloop(screen)

if __name__ == '__main__':
    # 배경 음악 무한 재생
    background_music.play(-1)
    show_start_menu()
