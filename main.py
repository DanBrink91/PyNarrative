import pygame
import pyscroll
from pytmx.util_pygame import load_pygame
screen_size = width, height = 320, 320

pygame.init()
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Some Game Demo')

# Load TMX data
tmx_data = load_pygame("maps/test.tmx")

# Make data source for the map
map_data = pyscroll.TiledMapData(tmx_data)

# Make the scrolling layer
map_layer = pyscroll.BufferedRenderer(map_data, screen_size)

# make the PyGame SpriteGroup with a scrolling map
group = pyscroll.PyscrollGroup(map_layer=map_layer)

# # Add sprites to the group
# group.add(sprite)

# # Center the layer and sprites on a sprite
# group.center(sprite.rect.center)


done = False

clock = pygame.time.Clock()

while not done:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True

	# Draw map
	group.draw(screen)

	# update
	pygame.display.flip()

	# limit to 60 fps
	clock.tick(60)

pygame.quit()