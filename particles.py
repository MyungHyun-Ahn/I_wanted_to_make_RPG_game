import pygame 
from support import import_folder
from random import choice

class AnimationPlayer:
    def __init__(self):
        self.frames = {
			# magic
			'flame': import_folder('resource/graphics/particles/flame/frames'),
			'aura': import_folder('resource/graphics/particles/aura'),
			'heal': import_folder('resource/graphics/particles/heal/frames'),
			'p_leaf_attack': import_folder('resource/graphics/particles/p_leaf_attack/frames'),
			'p_thunder': import_folder('resource/graphics/particles/p_thunder/frames'),
			
			# attacks 
			'claw': import_folder('resource/graphics/particles/claw'),
			'slash': import_folder('resource/graphics/particles/slash'),
			'sparkle': import_folder('resource/graphics/particles/sparkle'),
			'leaf_attack': import_folder('resource/graphics/particles/leaf_attack'),
			'thunder': import_folder('resource/graphics/particles/thunder'),
			'smoke': import_folder('resource/graphics/particles/smoke'),
			'flam': import_folder('resource/graphics/particles/flam'),
			'rock': import_folder('resource/graphics/particles/rock'),
			'smoke_orange': import_folder('resource/graphics/particles/smoke_orange'),
			'cut': import_folder('resource/graphics/particles/cut'),

			

			# monster deaths redraccoon
			'squid': import_folder('resource/graphics/particles/smoke_orange'),
			'raccoon': import_folder('resource/graphics/particles/raccoon'),
			'redraccoon': import_folder('resource/graphics/particles/redraccoon'),
			'spirit': import_folder('resource/graphics/particles/nova'),
			'bamboo': import_folder('resource/graphics/particles/bamboo'),
			'giantflam': import_folder('resource/graphics/particles/giantflam'),
			'frog': import_folder('resource/graphics/particles/frog'),
			'cyclope': import_folder('resource/graphics/particles/cyclope'),
			'greencyclope': import_folder('resource/graphics/particles/greencyclope'),
			'bluebutterfly': import_folder('resource/graphics/particles/bluebutterfly'),
			'minidragon': import_folder('resource/graphics/particles/minidragon'),
			'skull': import_folder('resource/graphics/particles/skull'),
			'demoncyclope': import_folder('resource/graphics/particles/demoncyclope'),

			
			# leafs 
			'leaf': (
				import_folder('resource/graphics/particles/leaf1'),
				import_folder('resource/graphics/particles/leaf2'),
				import_folder('resource/graphics/particles/leaf3'),
				import_folder('resource/graphics/particles/leaf4'),
				import_folder('resource/graphics/particles/leaf5'),
				import_folder('resource/graphics/particles/leaf6'),
				self.reflect_images(import_folder('resource/graphics/particles/leaf1')),
				self.reflect_images(import_folder('resource/graphics/particles/leaf2')),
				self.reflect_images(import_folder('resource/graphics/particles/leaf3')),
				self.reflect_images(import_folder('resource/graphics/particles/leaf4')),
				self.reflect_images(import_folder('resource/graphics/particles/leaf5')),
				self.reflect_images(import_folder('resource/graphics/particles/leaf6'))
				)
			}

    def reflect_images(self, frames):
        new_frames = []

        for frame in frames:
            flipped_frame = pygame.transform.flip(frame, True, False)
            new_frames.append(flipped_frame)

        return new_frames
    
    def create_grass_particles(self, pos, groups):
        animation_frames = choice(self.frames['leaf'])
        ParticleEffect(pos, animation_frames, groups)

    def create_particles(self, animation_type, pos, groups):
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos, animation_frames, groups)


class ParticleEffect(pygame.sprite.Sprite):
	def __init__(self, pos, animation_frames, groups) -> None:
		super().__init__(groups)
		self.sprite_type = 'magic'
		self.frame_index = 0
		self.animation_speed = 0.15
		self.frames = animation_frames
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(center = pos)

	def animate(self):
		self.frame_index += self.animation_speed
		if self.frame_index >= len(self.frames):
			self.kill()
		else:
			self.image = self.frames[int(self.frame_index)]
	
	def update(self):
		self.animate()
