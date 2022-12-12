# game setup
WIDTH    = 1280	
HEIGTH   = 720
FPS      = 60
TILESIZE = 64

# 게임 초기 세팅
MAPSIZE = 15
GRASSCOUNT = 5
OBJECTCOUNT = 1
ENTITYCOUNT = 1

# UI
BAR_HEIGHT       = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDHT = 200
EXP_BAR_WIDHT    = 800
ITEM_BOX_SIZE    = 80
UI_FONT          = 'resource/graphics/font/joystix.ttf'
UI_FONT_SIZE     = 18

# general colors
WATER_COLOR     = '#71ddee'
UI_BG_COLOR     = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR      = '#EEEEEE'

# ui colors
HEALTH_COLOR           = 'red'
ENERGY_COLOR           = 'blue'
EXP_COLOR              = 'yellow'
UI_BORDER_COLOR_ACTIVE = 'gold'

# upgrade menu
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'

# weapon
weapon_data = {
	'sword' : {'cooldown': 200, 'damage': 20, 'graphic': 'resource/graphics/weapons/sword/full.png'},
	'lance' : {'cooldown': 1000, 'damage': 80, 'graphic': 'resource/graphics/weapons/lance/full.png'},
	'axe'   : {'cooldown': 600, 'damage': 40, 'graphic': 'resource/graphics/weapons/axe/full.png'},
	'rapier': {'cooldown': 60,  'damage': 10, 'graphic': 'resource/graphics/weapons/rapier/full.png'},
	'sai'   : {'cooldown': 160,  'damage': 25, 'graphic': 'resource/graphics/weapons/sai/full.png'},
	'club'  : {'cooldown': 1200, 'damage': 90, 'graphic': 'resource/graphics/weapons/club/full.png'}
}

# item
item_data = {
	'lifepot':  {'type': 'hp', 'recovery': 30,  'graphic': 'resource/graphics/item/LifePot.png'},
	'medipack': {'type': 'hp', 'recovery': 60, 'graphic': 'resource/graphics/item/Medipack.png'},
	'waterpot': {'type': 'mp', 'recovery': 30,  'graphic': 'resource/graphics/item/WaterPot.png'}
}

# magic
magic_data = {
	'flame'         : {'strength': 5,  'cost': 20, 'graphic': 'resource/graphics/particles/flame/fire.png'},
	'p_thunder'     : {'strength': 20, 'cost': 30, 'graphic': 'resource/graphics/particles/p_thunder/p_thunder.png'},
	'p_leaf_attack' : {'strength': 15, 'cost': 25, 'graphic': 'resource/graphics/particles/p_leaf_attack/p_leaf_attack.png'},
	'heal'          : {'strength': 20, 'cost': 15, 'graphic': 'resource/graphics/particles/heal/heal.png'}
}

# enemy
monster_data = {
	# normal
	'squid'           : {'health': 100,  'exp': 150, 'damage': 13,  'attack_type': 'slash',       'attack_sound': 'resource/audio/attack/slash.wav'   , 'speed': 3, 'resistance': 3, 'attack_radius': 80,  'notice_radius': 360},
	'spirit'          : {'health': 100,  'exp': 130, 'damage': 8,   'attack_type': 'thunder',     'attack_sound': 'resource/audio/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60,  'notice_radius': 350},
	'bamboo'          : {'health': 70,   'exp': 120, 'damage': 6,   'attack_type': 'leaf_attack', 'attack_sound': 'resource/audio/attack/slash.wav'   , 'speed': 3, 'resistance': 3, 'attack_radius': 50,  'notice_radius': 300},
	'cyclope'         : {'health': 120,  'exp': 150, 'damage': 12,  'attack_type': 'rock',        'attack_sound': 'resource/audio/attack/rock.wav'   , 'speed': 4, 'resistance': 3, 'attack_radius': 50,  'notice_radius': 800},
	'greencyclope'    : {'health': 100,  'exp': 120, 'damage': 10,  'attack_type': 'rock',        'attack_sound': 'resource/audio/attack/rock.wav'   , 'speed': 4, 'resistance': 3, 'attack_radius': 50,  'notice_radius': 800},
	'bluebutterfly'   : {'health': 80,  'exp': 120,  'damage': 8,   'attack_type': 'smoke_orange', 'attack_sound': 'resource/audio/attack/frog.wav'   , 'speed': 3, 'resistance': 3, 'attack_radius': 50,  'notice_radius': 500},
	'minidragon'      : {'health': 110,  'exp': 140, 'damage': 10,  'attack_type': 'flam', 'attack_sound': 'resource/audio/attack/fire.wav'   , 'speed': 5, 'resistance': 3, 'attack_radius': 50,  'notice_radius': 600},
	'skull'           : {'health': 50,  'exp': 150, 'damage': 20,   'attack_type': 'cut', 'attack_sound': 'resource/audio/attack/claw.wav'   , 'speed': 6, 'resistance': 3, 'attack_radius': 40,  'notice_radius': 800},



	# boss
	'raccoon'      : {'health': 600, 'exp': 700,  'damage': 15, 'attack_type': 'claw',        'attack_sound': 'resource/audio/attack/claw.wav'    , 'speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 800},
	'redraccoon'   : {'health': 800, 'exp': 800,  'damage': 25, 'attack_type': 'claw',        'attack_sound': 'resource/audio/attack/claw.wav'    , 'speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 800},
	'giantflam'    : {'health': 900, 'exp': 1000, 'damage': 20, 'attack_type': 'flam',       'attack_sound': 'resource/audio/attack/fire.wav'    , 'speed': 3, 'resistance': 3, 'attack_radius': 130, 'notice_radius': 1000},
	'frog'         : {'health': 400, 'exp': 400,  'damage': 25, 'attack_type': 'smoke',       'attack_sound': 'resource/audio/attack/frog.wav'    , 'speed': 5, 'resistance': 3, 'attack_radius': 140, 'notice_radius': 1500},
	'demoncyclope'  : {'health': 700, 'exp': 900,  'damage': 30, 'attack_type': 'flam',       'attack_sound': 'resource/audio/attack/fire.wav'    , 'speed': 4, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 1500},
}

normal_monster_name = ['squid', 'spirit', 'bamboo', 'cyclope', 'bluebutterfly', 'minidragon', 'skull']
boss_monster_name = ['raccoon', 'redraccoon', 'giantflam', 'frog', 'demoncyclop']