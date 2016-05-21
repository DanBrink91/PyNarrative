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

class PlayerLayer(ScrollableLayer):
	def __init__(self):
		super(PlayerLayer, self).__init__()

		spritesheet = image.load('dude.png')
		frames = image.ImageGrid(spritesheet, 4, 3)
		self.sprite = Sprite(frames[10])
		# center on first tile
		self.sprite.position = self.sprite.width / 2, window_height - (self.sprite.height / 2)

		self.add(self.sprite)

player_layer = PlayerLayer()

MapLayer = load('test.tmx')['base']

scroller.add(MapLayer)
scroller.add(player_layer)

director.window.push_handlers(keyboard)
director.run(Scene(scroller))
