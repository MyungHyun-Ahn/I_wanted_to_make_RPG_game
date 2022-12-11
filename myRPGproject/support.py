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
def make_boundary_list(size: int): 
    boundary_list = [[-1] * size for _ in range(size)]

    for y in range(size):
        for x in range(size):
            if (y == 0 or x == 0) or (y == size - 1 or x == size - 1):
                boundary_list[y][x] = 'r'

    boundary_list[1][1] = 'p'

    return boundary_list



# 0, 1, 2, 3, 4
def make_grass_list(size: int, grass_num: int, boundary_list: list):
    grass_list = [[-1] * size for _ in range(size)]

    count = 0
    
    while True:
        random_x = randint(0, len(boundary_list) - 1)
        random_y = randint(0, len(boundary_list) - 1)

        if boundary_list[random_y][random_x] != -1:
            continue
        else:
            grass_list[random_y][random_x] = choice([8, 9, 10])
            count += 1
        
        if count == grass_num:
            break
    
    return grass_list


def make_object_list(size: int, obj_list: list, object_num: int, boundary_list: list, grass_list: list) -> list:
    object_list = [[-1] * size for _ in range(size)]

    count = 0
    
    while True:
        random_x = randint(0, len(boundary_list) - 1)
        random_y = randint(0, len(boundary_list) - 1)

        if boundary_list[random_y][random_x] != -1 or grass_list[random_y][random_x] != -1:
            continue
        else:
            object_list[random_y][random_x] = choice(obj_list)
            count += 1
        
        if count == object_num:
            break
    
    return object_list


"""
출현 몬스터 설정 
monster_list  : 출현 가능 몬스터 리스트
monster_num   : 출현 몬스터 수
boundary_list : 장애물 맵
390 : bamboo
391 : sprit
393 : squid
"""
def make_entity_list(size: int, monster_num: int, boundary_list: list, grass_list: list, object_list: list) -> list:
    entity_list = [[-1] * size for _ in range(size)]

    count = 0
    
    while True:
        random_x = randint(0, len(boundary_list) - 1)
        random_y = randint(0, len(boundary_list) - 1)

        if boundary_list[random_y][random_x] != -1 or grass_list[random_y][random_x] != -1 or object_list[random_y][random_x] != -1 or entity_list[random_y][random_x] != -1:
            continue
        else:
            entity_list[random_y][random_x] = 'm'
            count += 1
        
        if count == monster_num:
            break
    
    return entity_list

# n * n 사이즈의 미로 생성
# 단, n의 값으론 홀수만 입력 가능함
# 벽의 가장 자리는 항상 벽이어야 하므로
def generate_binary_tree_maze(n: int) -> list:
    binary_tree_maze_list = [[-1] * n for _ in range(n)]

    for y in range(n):
        for x in range(n):
            if y % 2 == 0 or x % 2 == 0:
                binary_tree_maze_list[y][x] = 'r'
            else:
                binary_tree_maze_list[y][x] = -1
    
    for y in range(n):
        for x in range(n):
            if y % 2 == 0 or x % 2 == 0:
                continue

            if x == n - 2 and y == n - 2:
                continue

            if x == n - 2:
                binary_tree_maze_list[y + 1][x] = -1
                continue

            if y == n - 2:
                binary_tree_maze_list[y][x + 1] = -1
                continue

            random_value = randint(0, 1)
            if random_value == 0:
                binary_tree_maze_list[y][x + 1] = -1
            else:
                binary_tree_maze_list[y + 1][x] = -1

    binary_tree_maze_list[1][1] = 'p'
    binary_tree_maze_list[n - 2][n - 2] = 'o' # 출구

    return binary_tree_maze_list


def list_to_csv(target_list: list, file_name: str):
    df = pd.DataFrame(target_list)
    df.to_csv("resource/map/{}.csv".format(file_name), header=None, index=None)


if __name__ == "__main__":
    boundary_list = generate_binary_tree_maze(51)
    list_to_csv(boundary_list, 'boundary')
    # grass_list = make_grass_list(50, 50, boundary_list)
    # list_to_csv(grass_list, 'grass')
    # object_list = make_object_list(50, [0, 1, 2, 3, 4], 30, boundary_list, grass_list)
    # list_to_csv(object_list, 'object')
    # entity_list = make_entity_list(50, [390, 391, 393], 50, boundary_list, grass_list, object_list)
    # list_to_csv(entity_list, 'entities')