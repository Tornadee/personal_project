# © Jason (Seojoon) Yeon 2018 October 17 ~
# statistical
import random
import math

class player:
	def __init__(self):
		self.x, self.z, self.r = 0.0, 0.0, 0.0

class platform:
	def __init__(self, x, z):
		self.x, self.z = x, z

class game:
	def __init__(self):
		self.platforms = []
		self.player = player()
		self.player_move_speed = 1.0
		self.player_steer_speed = 0.15
		self.platform_width = 1.8 # worked well with 1.75
		self.platform_length = 1
		self.step = 0
		self._build_platforms()

	def _reset(self):			# reset environment and variables
		self.player.x, self.player.z, self.player.r = 0.0, 0.0, 0.0
		self.step = 0

	def _step(self, action):		# apply action and return observation
		self.step += 1
		self.player.r += action * self.player_steer_speed
		self.player.x += math.sin(self.player.r) * self.player_move_speed
		self.player.z += math.cos(self.player.r) * self.player_move_speed
		done = False
		if (self._is_player_on_platform() == False):
			done = True
		next_state = self._return_state()
		return done, next_state

	def _build_platforms(self):	# building the map.
		map_data = [0,1,2,2,1,0,0,-1,-2,-3,-3,-2,-1,0,1,2,2,1,0,0,0]
		z = 0
		for i in range(len(map_data)):
			x = map_data[i] * 0.6
			z += 1
			self.platforms.append(platform(x,z))

	def _is_player_on_platform(self):	# player dead or alive??
		for i in range(len(self.platforms)):
			platform = self.platforms[i]
			# sides of the platform
			plat_left = platform.x - self.platform_width/2
			plat_right = platform.x + self.platform_width/2
			plat_far = platform.z + self.platform_length/2
			plat_close = platform.z - self.platform_length/2
			# position of player
			px = self.player.x
			pz = self.player.z
			if ((px >= plat_left) and (px <= plat_right) and (pz <= plat_far) and (pz >= plat_close)):
				return True
				break
		return False

	def _return_state(self):	# observation
		# player position and rotations
		p_x = self.player.x
		p_z = self.player.z
		p_r = self.player.r
		# upcoming platform relative positions
		blockind_1 = round((p_z - 1))
		b_1 = self.platforms[blockind_1]
		blockind_2 = round((p_z))
		b_2 = self.platforms[blockind_2]
		# differences in X coordinates
		d_1_x = p_x - b_1.x
		d_2_x = p_x - b_2.x
		# data normalization
		p_z /= 10
		p_x /= 2
		d_1_x /= 2
		d_2_x /= 2
		p_x += 0.5
		d_1_x += 0.5
		d_2_x += 0.5
		# return
		return p_x, p_z, p_r, d_1_x, d_2_x
