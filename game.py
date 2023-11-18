# title:   Bloom Blaster
# author:  Hevanafa
# desc:    Farming simulator
# license: MIT License
# version: 0.1
# script:  python

from typings import btn, circ, circb, cls, key, keyp, poke, rect, rectb, spr, mouse

def getDist(x1: float, x2: float, y1: float, y2: float):
	return (x2 - x1) ** 2 + (y2 - y1) ** 2

sw = 240
sh = 136

p_cx = sw / 2
p_cy = sh / 2

toolbar_start = sw // 2 - 100

# p_grid_x = 12
# p_grid_y = 5
P_MAX_REACH = 1024
P_MAX_WATER = 4
p_water = P_MAX_WATER
p_money = 0

well_cx = sw / 2
well_cy = sh - 20

TOOL_SHOVEL = 0
TOOL_PAIL = 1
TOOL_SEEDS = 2
TOOL_SICKLE = 3

p_active_tool = 0


class Soil:
	def __init__(self, mx = -1, my = -1):
		self.grid_x = getGridN(mx)
		self.grid_y = getGridN(my)
		self.watered = False
		self.has_seeds = False
		self.growth_stage = 0  # only increases when there are seeds

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
	global t, p_cx, p_cy, p_grid_x, p_grid_y, p_active_tool
	global p_water, well_cx, well_cy
	global last_mleft

	# hide mouse cursor
	poke(0x3ffb, 0)

	if keyp(28): p_active_tool = TOOL_SHOVEL
	if keyp(29): p_active_tool = TOOL_PAIL
	if keyp(30): p_active_tool = TOOL_SEEDS
	if keyp(31): p_active_tool = TOOL_SICKLE

	if key(23):
		p_cy -= 0.5
	if key(19):
		p_cy += 0.5

	if key(1):
		p_cx -= 0.5
	if key(4):
		p_cx += 0.5

	if keyp(49): # TAB
		pass


	# check mouse inputs
	mx, my, mleft, *_ = mouse()
	
	if mleft != last_mleft:
		last_mleft = mleft

		if mleft:
			if toolbar_start <= mx and mx <= toolbar_start + 17 * 4:
				p_active_tool = (mx - toolbar_start) // 17

			if getDist(mx, p_cx, my, p_cy) <= P_MAX_REACH:
				# Note: match-case isn't supported
				if p_active_tool == TOOL_SHOVEL:
					soil = findSoilPatch(mx, my)

					if soil is None:
						soil_patches.append(Soil(mx, my))
				elif p_active_tool == TOOL_PAIL:
					if p_water > 0:
						soil = findSoilPatch(mx, my)

						if soil and not soil.watered:
							p_water -= 1
							soil.watered = True
				elif p_active_tool == TOOL_SEEDS:
					soil = findSoilPatch(mx, my)

					if soil:
						soil.has_seeds = True

	if p_water < P_MAX_WATER and p_active_tool == 1 and getDist(well_cx, p_cx, well_cy, p_cy) < 100:
		p_water = P_MAX_WATER

	for soil in soil_patches:
		if soil.has_seeds and soil.watered and soil.growth_stage < 240:
			soil.growth_stage += 1


	cls(5)

	# well
	circb(int(well_cx), int(well_cy), 10, 12)
	spr(7, int(well_cx - 8), int(well_cy), 11, w=2, h=2)

	# soil patches
	for soil in soil_patches:
		spr(soil.watered and 66 or 65, soil.grid_x * 8, soil.grid_y * 8)

		if soil.has_seeds:
			spr(69 + soil.growth_stage // 60, soil.grid_x * 8, soil.grid_y * 8, 0)

	# highlight tile
	if getDist(mx, p_cx, my, p_cy) < P_MAX_REACH:
		block_x, block_y = mx // 8 * 8, my // 8 * 8
		rectb(block_x, block_y, 8, 8, 7)

	# player sprite
	spr(1, int(p_cx - 4), int(p_cy - 4), 11, w=2, h=2)

	# toolbar
	for a in range(0, 4):
		x = toolbar_start + a * 17
		y = sh - 20

		rectb(x - 1, y - 1, 18, 18, 1)

		spr(81 + a, x, y, 0, 2)

	for a in range(0, 2):
		rectb(
			sw // 2 - 101 + p_active_tool * 17 - a,
			sh - 21 - a,
			18 + a * 2, 18 + a * 2,
			7)

	# water progress bar
	spr(40, 4, 4, 0)
	perc = p_water / P_MAX_WATER
	rect(15, 5, round(perc * 20), 6, 12)
	rectb(15, 5, 20, 6, 7)

	
	# mouse cursor
	spr(80, mx - 1, my - 1, 11)

