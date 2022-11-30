from csv import reader
from os import walk
import pygame
import pandas as pd
from random import randint, choice

def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter = ',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map

def import_folder(path):
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


# 맵의 틀
def make_boundary_list(n: int): 
    boundary_list = [[-1] * 50 for _ in range(50)]

    for y in range(n):
        for x in range(n):
            if (y == 0 or x == 0) or (y == n - 1 or x == n - 1):
                boundary_list[y][x] = 'r'

    boundary_list[1][1] = 'p'

    return boundary_list
    
"""
출현 몬스터 설정 
monster_list  : 출현 가능 몬스터 리스트
monster_num   : 출현 몬스터 수
boundary_list : 장애물 맵
390 : bamboo
391 : sprit
393 : squid
"""
def make_entity_list(monster_list: list, monster_num: int, boundary_list: list):
    entity_list = [[-1] * 50 for _ in range(50)]

    count = 0
    
    while True:
        random_x = randint(0, len(boundary_list) - 1)
        random_y = randint(0, len(boundary_list) - 1)

        if boundary_list[random_y][random_x] != -1:
            continue
        else:
            entity_list[random_y][random_x] = choice(monster_list)
            count += 1
            print('몬스터 생성 성공')
        
        if count == monster_num:
            break
    
    return entity_list


def list_to_csv(target_list: list, file_name: str):
    df = pd.DataFrame(target_list)
    df.to_csv("resource/map/{}.csv".format(file_name), header=None, index=None)

def generate_binary_tree_maze(n: int) -> list:
    binary_tree_maze_list = [[-1] * n for _ in range(n)]

    for y in range(n):
        for x in range(n):
            if y % 2 == 0 or x % 2 == 0:
                binary_tree_maze_list[y][x] = 'r'
            else:
                binary_tree_maze_list[y][x] = '1'
    

    for y in range(n):
        for x in range(n):
            if y % 2 == 0 or x % 2 == 0:
                continue

            if x == n - 2 and y == n - 2:
                continue

            if x == n - 2:
                binary_tree_maze_list[y + 1][x] = '1'
                continue

            if y == n - 2:
                binary_tree_maze_list[y][x + 1] = '1'
                continue

            random_value = randint(0, 1)
            if random_value == 0:
                binary_tree_maze_list[y][x + 1] = '1'
            else:
                binary_tree_maze_list[y + 1][x] = '1'


    binary_tree_maze_list[1][1] = 'p'
    binary_tree_maze_list[n - 2][n - 2] = 'o' # 출구

    return binary_tree_maze_list


if __name__ == "__main__":
    boundary_list = generate_binary_tree_maze(51)
    list_to_csv(boundary_list, 'boundary')
    entity_list = make_entity_list([390, 391, 392, 393], 5, boundary_list)
    list_to_csv(entity_list, 'entities')