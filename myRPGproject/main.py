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

        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('black')
            # 디버그 왼쪽 상단에 메세지 출력
            # debug('hello :)')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
	game = Game()
	game.run()