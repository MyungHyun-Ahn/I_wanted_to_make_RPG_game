import pygame
pygame.init()
font = pygame.font.Font(None, 30)

# y, x 기본값 10, 10
def debug(info,y = 10, x = 10):
	display_surface = pygame.display.get_surface()
	# 흰글씨
	debug_surf = font.render(str(info), True, 'White')
	# 왼쪽 정렬로 출력
	debug_rect = debug_surf.get_rect(topleft = (x,y))
	pygame.draw.rect(display_surface, 'Black', debug_rect)
	display_surface.blit(debug_surf, debug_rect)
