# 게임의 기본 세팅 값
WIDTH    = 1280	     # 가로
HEIGTH   = 720       # 세로
FPS      = 60        # FPS
TILESIZE = 64        # 타일 사이즈

# UI
BAR_HEIGHT       = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDHT = 140
ITEM_BOX_SIZE    = 80
UI_FONT          = 'resource/graphics/font/joystix.ttf'
UI_FONT_SIZE     = 18

# general colors
WATER_COLOR     = '#71ddee'
UI_BG_COLOR     = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR      = '#EEEEEE'

# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# 월드 맵
# 'x' : 돌 혹은 벽
# 'p' : 플레이어 위치
# ' ' : 플레이어가 걸을 수 있는 위치
#               y, x
# [0][0] 좌표 : 0, 0
# [0][1] 좌표 : 0, 64
# [1][0] 좌표 : 64, 0
# [y][x] 좌표 : 64 * y, 64 * x 
WORLD_MAP = [
['x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ','p',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ','x',' ',' ',' ',' ',' ','x','x','x','x','x',' ',' ',' ',' ',' ','x'],
['x',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ','x'],
['x',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ','x'],
['x',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ','x'],
['x',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ','x'],
['x',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ','x'],
['x',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ','x'],
['x',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ','x'],
['x',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ','x','x','x',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ','x',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ','x','x','x','x','x',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ','x','x','x',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x'],
]

# weapon
weapon_data = {
	'sword': {'cooldown': 100, 'damage': 15,'graphic':'resource/graphics/weapons/sword/full.png'},
	'lance': {'cooldown': 400, 'damage': 30,'graphic':'resource/graphics/weapons/lance/full.png'},
	'axe': {'cooldown': 300, 'damage': 20, 'graphic':'resource/graphics/weapons/axe/full.png'},
	'rapier':{'cooldown': 50, 'damage': 8, 'graphic':'resource/graphics/weapons/rapier/full.png'},
	'sai':{'cooldown': 80, 'damage': 10, 'graphic':'resource/graphics/weapons/sai/full.png'}
}

# magic
magic_data = {
	'flame': {'strength': 5,'cost': 20,'graphic':'resource/graphics/particles/flame/fire.png'},
	'heal' : {'strength': 20,'cost': 10,'graphic':'resource/graphics/particles/heal/heal.png'}
}