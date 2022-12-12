import pygame
from settings import *
from player import Player

class Upgrade:
    def __init__(self, player: Player) -> None:
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_nr = len(player.stats)
        self.attribute_names = list(player.stats.keys())
        self.max_values = list(player.max_stats.values())
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # upgrade menu
        self.height = (self.display_surface.get_size()[1] - 200)// 6
        self.width = self.display_surface.get_size()[0] * 0.6
        self.create_items()
        
        # selection system
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True
    
    def input(self):
        keys = pygame.key.get_pressed()

        if self.can_move:
            if keys[pygame.K_DOWN] and self.selection_index < self.attribute_nr - 1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_UP] and self.selection_index >= 1:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            if keys[pygame.K_SPACE]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.item_list[self.selection_index].trigger(self.player)

    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 300:
                self.can_move = True

    def create_items(self):
        self.item_list = []

        for item, index in enumerate(range(self.attribute_nr)):
            # horizontal position
            full_height = self.display_surface.get_size()[1] - 200
            increment = full_height // self.attribute_nr
            top = (item * increment) + (increment - self.height) // 2 + 100

            # vertical position
            left = self.display_surface.get_size()[0] * 0.2

            # create the object
            item = UpgradeMenu(left, top, self.width, self.height, index, self.font)
            self.item_list.append(item)

    def display_main(self):
        font1 = pygame.font.Font(UI_FONT, 25)
        title_rect = pygame.Rect(580, 20, 150, 80)


        pygame.draw.rect(self.display_surface, UI_BG_COLOR, title_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, title_rect, 4)

        title_surf = font1.render('status', False, TEXT_COLOR)
        title_rect = title_surf.get_rect(center = title_rect.center)
        self.display_surface.blit(title_surf, title_rect)

        font2 = pygame.font.Font(UI_FONT, 10)
        stat_point_rect = pygame.Rect(self.display_surface.get_size()[0] - 405, self.display_surface.get_size()[1] - 100, 150, 60)

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, stat_point_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, stat_point_rect, 4)

        stat_point_surf = font2.render('stat point : {}'.format(self.player.stat_point), False, TEXT_COLOR)
        stat_point_rect = stat_point_surf.get_rect(center = stat_point_rect.center)
        self.display_surface.blit(stat_point_surf, stat_point_rect)




    def display(self):
        self.input()
        self.selection_cooldown()

        self.display_main()

        for index, item in enumerate(self.item_list):
            # get attributes
            name = self.attribute_names[index]
            stat = self.player.stats[name]
            rate = self.player.upgrade_rate[name]
            item.display(self.display_surface,self.selection_index,name, rate, stat)


class UpgradeMenu:
    def __init__(self, l, t, w, h, index, font) -> None:
        self.rect = pygame.Rect(l, t, w, h)
        self.index = index
        self.font = font
        self.w = w
        self.h = h

        self.sounds = {
            'success' : pygame.mixer.Sound('resource/audio/Accept.wav'),
            'failure' : pygame.mixer.Sound('resource/audio/Cancel.wav'),
        }


    def display_names(self, surface, name, stat, rate, selected):
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR

        # title
        title_surf = self.font.render('{} : {}'.format(name, stat), False, color)
        title_rect = title_surf.get_rect(midleft = self.rect.midleft + pygame.math.Vector2(20, 0))

        # cost
        rate_surf = self.font.render('+{}'.format(rate), False, color)
        rate_rect = rate_surf.get_rect(midright = self.rect.midright - pygame.math.Vector2(40, 0))

        # draw
        surface.blit(title_surf, title_rect)
        surface.blit(rate_surf, rate_rect)

    def display_bar(self, surface, value, max_value, selected):
        # drawing setup
        top = self.rect.midtop + pygame.math.Vector2(0, 60)
        bottom = self.rect.midbottom - pygame.math.Vector2(0, 60)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR

        # bar setup
        full_height = bottom[1] - top[1]
        relative_number = (value / max_value) * full_height
        value_rect = pygame.Rect(top[0] - 15, bottom[1] - relative_number, 30, 10)

        # draw elements
        pygame.draw.line(surface, color, top, bottom, 5)
        pygame.draw.rect(surface, color, value_rect)

    def trigger(self, player: Player):
        upgrade_attribute = list(player.stats.keys())[self.index]

        if player.stat_point >= 1 and player.stats[upgrade_attribute] < player.max_stats[upgrade_attribute]:
            self.sounds['success'].play() # 스텟 업그레이드 성공시 재생
            player.stat_point -= 1
            player.stats[upgrade_attribute] += player.upgrade_rate[upgrade_attribute]
            if upgrade_attribute == 'health':
                player.health += player.upgrade_rate[upgrade_attribute]
        else:
            self.sounds['failure'].play() # 실패시 재생

        if player.stats[upgrade_attribute] > player.max_stats[upgrade_attribute]:
            player.stats[upgrade_attribute] = player.max_stats[upgrade_attribute]

    def display(self, surface, selection_num, name, rate, stat):
        if self.index == selection_num:
            pygame.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
        else:
            pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
        
        self.display_names(surface, name, stat, rate, self.index == selection_num)

