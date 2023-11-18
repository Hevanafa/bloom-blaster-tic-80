# title:   Bloom Blaster
# author:  Hevanafa
# desc:	short description
# license: MIT License
# version: 0.1
# script:  python

from typings import btn, cls, key, keyp, poke, rectb, spr, mouse

def getDist(x1: float, x2: float, y1: float, y2: float):
	return (x2 - x1) ** 2 + (y2 - y1) ** 2

sw = 240
sh = 136

px = sw / 2
py = sh / 2

p_grid_x = 12
p_grid_y = 5
p_water = 0
p_money = 0

p_active_tool = 0

class Soil:
	def __init__(self, mx = -1, my = -1):
		self.grid_x = getGridN(mx)
		self.grid_y = getGridN(my)
		self.watered = False
		self.has_seeds = False

soil_patches: list[Soil] = []


def getGridN(x: float) -> int:
	return x // 8

def findSoilPatch(mx: int, my: int) -> Soil:
	for soil in soil_patches:
		if (soil.grid_x == getGridN(mx)) and (soil.grid_y == getGridN(my)):
			return soil
		
	return None


last_mleft = False

def TIC():
	global t, px, py, p_grid_x, p_grid_y, p_active_tool
	global last_mleft

	# hide mouse cursor
	poke(0x3ffb, 0)

	if keyp(28): p_active_tool = 0
	if keyp(29): p_active_tool = 1
	if keyp(30): p_active_tool = 2
	if keyp(31): p_active_tool = 3

	if key(23):
		py -= 0.5
	if key(19):
		py += 0.5

	if key(1):
		px -= 0.5
	if key(4):
		px += 0.5

	if keyp(49): # TAB
		pass


	mx, my, mleft, *_ = mouse()
	
	if mleft != last_mleft:
		last_mleft = mleft

		skip = False

		if getDist(mx, px, my, py) <= 1600:
			# Note: match-case isn't supported
			if p_active_tool == 0:
				soil = findSoilPatch(mx, my)

				if soil is None:
					soil_patches.append(Soil(mx, my))
			elif p_active_tool == 1:
				soil = findSoilPatch(mx, my)

				if soil:
					soil.watered = True
			elif p_active_tool == 2:
				soil = findSoilPatch(mx, my)

				if soil:
					soil.has_seeds = True


	cls(0)

	# soil patches
	for soil in soil_patches:
		spr(soil.watered and 66 or 65, soil.grid_x * 8, soil.grid_y * 8)

		if soil.has_seeds:
			spr(67, soil.grid_x * 8, soil.grid_y * 8, 0)

	# highlight tile
	if getDist(mx, px, my, py) < 1600:
		block_x, block_y = mx // 8 * 8, my // 8 * 8
		rectb(block_x, block_y, 8, 8, 7)

	# player sprite
	spr(1, int(px), int(py), 11, w=2, h=2)

	# toolbar
	for a in range(0, 4):
		x = sw // 2 - 100 + a * 17
		y = sh - 20

		rectb(x - 1, y - 1, 18, 18, 5)

		spr(81 + a, x, y, 0, 2)

	rectb(sw // 2 - 101 + p_active_tool * 17, sh - 21, 18, 18, 7)
	
	# mouse cursor
	spr(80, mx - 1, my - 1, 11)

