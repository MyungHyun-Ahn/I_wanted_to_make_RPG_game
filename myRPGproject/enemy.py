import pygame
from player import Player
from settings import *
from entity import Entity
from support import *
from typing import Callable

class Enemy(Entity):
    def __init__(self, monster_name: str, monster_type: str, game_round: int, map_size: int, pos: tuple, groups: list, obstacle_sprites: pygame.sprite.Group, damage_player: Callable, trigger_death_particles: Callable, monster_count_down: Callable, drop_item: Callable, add_exp: Callable, drop_weapon: Callable) -> None:
        # general setup
        super().__init__(groups)
        self.sprite_type = 'enemy'
        self.monster_type  = monster_type
        self.display_surface = pygame.display.get_surface()

        # graphics setup
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.image  = self.animations[self.status][self.frame_index]

        # movement
        self.rect             = self.image.get_rect(topleft = pos)
        self.hitbox           = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

        # stats
        self.monster_name  = monster_name
        monster_info       = monster_data[self.monster_name]
        self.health        = monster_info['health'] + monster_info['health'] * (game_round / 5)
        self.max_health = self.health
        self.exp           = monster_info['exp'] + monster_info['exp'] * (game_round / 5)
        self.speed         = monster_info['speed']
        self.attack_damage = monster_info['damage'] + monster_info['damage'] * (game_round / 5)
        self.resistance    = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type   = monster_info['attack_type']

        # player interaction
        self.can_attack              = True
        self.attack_time             = None
        self.attack_cooldown         = 400
        self.damage_player           = damage_player
        self.trigger_death_particles = trigger_death_particles
        self.add_exp = add_exp

        # level interaction
        self.monster_count_down = monster_count_down

        # invincibility timer
        self.vulnerable             = True
        self.hit_time               = None
        self.invincibility_duration = 300

        self.drop_item = drop_item
        self.drop_weapon = drop_weapon
        self.map_size = map_size

        # sounds
        self.death_sound = pygame.mixer.Sound('resource/audio/death.wav')
        self.hit_sound = pygame.mixer.Sound('resource/audio/hit.wav')
        self.attack_sound = pygame.mixer.Sound(monster_info['attack_sound'])
        self.death_sound.set_volume(0.6)
        self.hit_sound.set_volume(0.6)
        self.attack_sound.set_volume(0.6)
        
    def import_graphics(self, name: str):
        if self.monster_type == 'normal':
            self.animations = {
                'idle'         : [],
                'up'           : [],
                'down'         : [],
                'left'         : [],
                'right'        : [],
                'attack'       : []
            }
        elif self.monster_type == 'unique':
            self.animations = {
            'idle'  : [],
            'move'  : [],
            'attack': []
            }
        

        main_path = 'resource/graphics/monsters/{}/'.format(name)
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def get_player_distance_direction(self, player: Player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
            # print(direction)
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)
    
    def get_status(self, player: Player):
        distance = self.get_player_distance_direction(player)[0]
        direction = self.get_player_distance_direction(player)[1]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            if self.monster_type == 'normal':
            # 위쪽
                if (direction.x < 0.5 and direction.x > -0.5) and direction.y < -0.5:
                    self.status = 'up'
                # 아래쪽
                elif (direction.x < 0.5 and direction.x > -0.5) and direction.y > 0.5:
                    self.status = 'down'
                # 오른쪽
                elif direction.x >= 0.5 and (direction.y <= 0.5 and direction.y >= -0.5):
                    self.status = 'right'
                # 왼쪽
                elif direction.x <= -0.5 and (direction.y <= 0.5 and direction.y >= -0.5):
                    self.status = 'left'
            else:
                self.status = 'move'
        else:
            self.status = 'idle'
    
    def actions(self, player: Player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
            self.attack_sound.play()
        elif self.status == 'up' or self.status == 'down' or self.status == 'right' or self.status == 'left' or self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def get_damage(self, player: Player, attack_type: str):
        if self.vulnerable:
            self.hit_sound.play()
            self.direction = self.get_player_distance_direction(player)[1]
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()
            else:
                self.health -= player.get_full_magic_damage()
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False
        
    def check_death(self):
        if self.health <= 0:
            self.kill()
            self.trigger_death_particles(self.rect.center, self.monster_name)
            self.death_sound.play()
            self.monster_count_down()
            if self.monster_type == 'normal':
                self.drop_item(self.rect.center)
            else:
                self.drop_weapon(self.rect.center)
            self.add_exp(self.exp)
    
    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def health_ui(self, pos):
        # show_bar(self, current, max_amount, bg_rect, color):
        # draw bg
        x = pos[0]
        y = pos[1] - 10
        if self.monster_type == 'normal':
            bg_rect = pygame.Rect(x, y, 64, 10)
        else:
            bg_rect = pygame.Rect(x, y, 240, 20)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # converting stat to pixel
        ratio = self.health / self.max_health
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # drawing the bar
        pygame.draw.rect(self.display_surface, 'red', current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)


    def update(self):
        # print(self.hitbox.x, self.hitbox.y)
        self.hit_reaction()
        self.out_map()
        self.move(self.speed)
        self.animate()
        self.cooldown()
        self.check_death()

    def enemy_update(self, player: Player, pos) -> None:
        self.get_status(player)
        self.actions(player)
        self.health_ui(pos)

