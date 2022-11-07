import pygame, os

DIR_PATH = os.path.dirname(__file__)
DIR_IMAGE = os.path.join(DIR_PATH, 'resource/image')
DIR_SOUND = os.path.join(DIR_PATH, 'resource/sound')

class SpriteSheet:
    def __init__(self, filename, width, height, max_row, max_col, max_index) -> None:
        # 스프레드시트 이미지 로드
        baseImage = pygame.image.load(os.path.join(DIR_IMAGE, filename))

        # 스프레드시트를 자르고 하나씩 추가할 리스트
        self.spr = []

        for i in range(max_index):
            image = pygame.Surface((width, height))
            image.blit(baseImage, (0, 0), ((i % width) * width, (i / max_row) * height, width, height))
            image_scaled = pygame.transform.scale(image, (width * 4, height * 4))
            self.spr.append(image_scaled)

        