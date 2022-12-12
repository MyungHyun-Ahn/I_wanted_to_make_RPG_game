import pygame
from settings import *
from player import Player

class UI:
    def __init__(self) -> None:
        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(73, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(73, 34, ENERGY_BAR_WIDHT, BAR_HEIGHT)
        self.exp_bar_rect    = pygame.Rect(self.display_surface.get_size()[0] - 1000, self.display_surface.get_size()[1] - 30, EXP_BAR_WIDHT, BAR_HEIGHT)

        self.plus_icon = pygame.image.load('resource/graphics/icon/plus.png').convert_alpha()
        self.ticks = 0
        self.plus_icon_show = True

        # convert weapon dictionary
        # weapon 딕셔너리를 변환
        self.weapon_grahics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_grahics.append(weapon)

        # convert magic dictionary
        self.magic_graphics = []
        for magic in magic_data.values():
            magic = pygame.image.load(magic['graphic']).convert_alpha()
            self.magic_graphics.append(magic)

    def show_bar(self, current, max_amount, bg_rect, color):
        # draw bg
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # converting stat to pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # drawing the bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_exp(self, exp, level_up_exp):
        per = round((exp / level_up_exp) * 100, 3)
        text_surf = self.font.render(str(per), False, TEXT_COLOR)
        x = self.exp_bar_rect.centerx
        y = self.exp_bar_rect.centery + 10
        text_rect = text_surf.get_rect(bottomright = (x, y))

        # pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(10, 10))
        self.display_surface.blit(text_surf, text_rect)
        # pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(10, 10), 3)

    def show_level(self, level):
        font = pygame.font.Font(UI_FONT, 14)
        text_surf = font.render("LV.{}".format(int(level)), False, TEXT_COLOR)
        x = 60
        y = 42
        text_rect = text_surf.get_rect(bottomright = (x, y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)

    def selection_box(self, left, top):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

        return bg_rect

    def weapon_overlay(self, weapon_index):
        bg_rect = self.selection_box(10, 600)
        weapon_surf = self.weapon_grahics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center = bg_rect.center)

        self.display_surface.blit(weapon_surf, weapon_rect)

    def magic_overlay(self):
        for i in range(4):
            bg_rect = self.selection_box(100 + i * 90, 600)
            magic_surf = self.magic_graphics[i]
            magic_rect = magic_surf.get_rect(center = bg_rect.center)
            self.display_surface.blit(magic_surf, magic_rect)

    def monster_count(self, monster_count):
        text_surf = self.font.render("remaining monsters : {}".format(monster_count), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 100
        y = 40
        text_rect = text_surf.get_rect(bottomright = (x, y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)

    def draw_round(self, game_round: int):
        font = pygame.font.Font(UI_FONT, 60)

        text_surf = font.render("Round {}".format(game_round), False, TEXT_COLOR)
        x = 640
        y = 360
        
        text_rect = text_surf.get_rect(center = (x, y))


        surf_rect = text_rect.inflate(20, 20)
        rect_width = surf_rect.width
        rect_height = surf_rect.height

        surface = pygame.Surface((rect_width, rect_height))
        pygame.draw.rect(surface, UI_BG_COLOR, surf_rect)
        surface.set_alpha(170)
        self.display_surface.blit(surface, surf_rect)
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(surface, UI_BORDER_COLOR, surf_rect, 3)

    
    def draw_clear(self, ticks: int):
        font = pygame.font.Font(UI_FONT, 60)

        text_surf = font.render("Clear", False, TEXT_COLOR)
        text_surf2 = self.font.render("next stage starts in {} second".format(ticks), False, TEXT_COLOR)

        x = 640
        y = 360

        x2 = 640
        y2 = 425

        text_rect = text_surf.get_rect(center = (x, y))

        surf_rect = text_rect.inflate(20, 20)
        rect_width = surf_rect.width
        rect_height = surf_rect.height

        surface = pygame.Surface((rect_width, rect_height))
        surface.set_alpha(170)

        text_rect2 = text_surf2.get_rect(center = (x2, y2))

        surf_rect2 = text_rect2.inflate(20, 20)
        rect_width2 = surf_rect2.width
        rect_height2 = surf_rect2.height

        surface2 = pygame.Surface((rect_width2, rect_height2))
        surface2.set_alpha(170)

        pygame.draw.rect(surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surface.blit(surface, surf_rect)
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)

        pygame.draw.rect(surface2, UI_BG_COLOR, text_rect2.inflate(20, 20))
        self.display_surface.blit(surface2, surf_rect2)
        self.display_surface.blit(text_surf2, text_rect2)
        pygame.draw.rect(surface2, UI_BORDER_COLOR, text_rect2.inflate(20, 20), 3)

    def draw_game_over(self):
        font = pygame.font.Font(UI_FONT, 60)

        text_surf = font.render("game over", False, TEXT_COLOR)

        x = 640
        y = 360

        text_rect = text_surf.get_rect(center = (x, y))

        surf_rect = text_rect.inflate(20, 20)
        rect_width = surf_rect.width
        rect_height = surf_rect.height

        surface = pygame.Surface((rect_width, rect_height))

        pygame.draw.rect(surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surface.blit(surface, surf_rect)
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)

    def show_have_statpoint(self, player: Player):
        if player.stat_point > 0 and self.plus_icon_show == True:
            self.display_surface.blit(self.plus_icon, (273, 13))
        if self.ticks % 25 == 0:
            self.plus_icon_show = not self.plus_icon_show
        self.ticks += 1
        

        

    def display(self, player: Player, monster_count: int):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)
        self.show_bar(player.exp, player.level_up_exp, self.exp_bar_rect, EXP_COLOR)
        self.show_have_statpoint(player)

        self.show_exp(player.exp, player.level_up_exp)
        self.show_level(player.level)

        self.monster_count(monster_count)
        
        self.weapon_overlay(player.weapon_index)
        self.magic_overlay()