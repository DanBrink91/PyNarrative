from cocos.actions import Action
from cocos.sprite import Sprite
from cocos.tiles import load
from cocos.layer import ScrollingManager, ScrollableLayer
from cocos.director import director
from cocos.scene import Scene

from pyglet.window import key
from pyglet import image

window_width, window_height = 320, 320
director.init(width=320, height=320)
scroller = ScrollingManager()
keyboard = key.KeyStateHandler()

class PlayerSprite(Sprite):
	# facing
	UP = 0
	RIGHT = 1
	DOWN = 2
	LEFT = 3

	def __init__(self, facing=2):
		spritesheet = image.load('dude.png')
		frames = image.ImageGrid(spritesheet, 4, 3)
		super(PlayerSprite, self).__init__(frames[10])
		
		self.facing = facing
		self.animating = False

		self.up = image.Animation.from_image_sequence(frames[:2], 0.7, False)
		self.right =  image.Animation.from_image_sequence(frames[3:5], 0.7, False)
		self.left =  image.Animation.from_image_sequence(frames[6:9], 0.7, False)
		self.down = image.Animation.from_image_sequence(frames[10:], 0.7, False)
		# center on first tile
		self.position = self.width / 2, window_height - (self.height / 2)

	def animate(self, direction):
		if direction == self.facing and self.animating:
			return
		print "animating"
		self.animating = True
		self.facing = direction

		if direction == PlayerSprite.UP:
			self.image = self.up
		elif direction == PlayerSprite.DOWN:
			self.image = self.down
		elif direction == PlayerSprite.RIGHT:
			self.image = self.right
		elif direction == PlayerSprite.LEFT:
			self.image = self.left

	def on_animation_end(self):
		self.animating = False

class PlayerAction(Action):
	# pretty much __init__ for action
	def start(self):
		self.target.velocity = 0, 0

	def step(self, dt):
		old_dx = self.target.velocity[0]
		old_dy = self.target.velocity[1]

		dx = (keyboard[key.RIGHT] - keyboard[key.LEFT]) * 100 * dt
		dy = (keyboard[key.UP] - keyboard[key.DOWN]) * 100 * dt

		if dx > 0 :
			self.target.animate(self.target.RIGHT)
		elif dx < 0 :
			self.target.animate(self.target.LEFT)
		elif dy > 0 :
			self.target.animate(self.target.UP)
		elif dy < 0:
			self.target.animate(self.target.DOWN)



		position = self.target.get_rect().copy() # get rekt
		position.x += dx
		position.y += dy

		self.target.position = position.center

		scroller.set_focus(*position.center)


class PlayerLayer(ScrollableLayer):
	def __init__(self):
		super(PlayerLayer, self).__init__()

		spritesheet = image.load('dude.png')
		frames = image.ImageGrid(spritesheet, 4, 3)
		
		self.sprite = PlayerSprite()

		self.add(self.sprite)
		self.sprite.do(PlayerAction())

player_layer = PlayerLayer()

MapLayer = load('test.tmx')['base']

scroller.add(MapLayer)
scroller.add(player_layer)

director.window.push_handlers(keyboard)
director.run(Scene(scroller))
