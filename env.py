# statistical
import random
import math
import numpy as np

# data visualization
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

class player:
	def __init__(self):
		self.x, self.z, self.r = 0.0, 0.0, 0.0;

class platform:
	def __init__(self, x, z):
		self.x, self.z = x, z;

class game:
	def __init__(self):
		self.platforms = [];
		self.player = player();
		self.player_move_speed = 1.0;
		self.player_steer_speed = 0.15;
		self.platform_width = 1.8; # worked well with 1.75;
		self.platform_length = 1;
		self.step = 0;
		self._build_platforms();

	def _reset(self):			# reset environment and variables
		self.player.x, self.player.z, self.player.r = 0.0, 0.0, 0.0;
		self.step = 0;

	def _step(self, action):		# apply action and return observation
		self.step += 1;
		self.player.r += action * self.player_steer_speed;
		self.player.x += math.sin(self.player.r) * self.player_move_speed;
		self.player.z += math.cos(self.player.r) * self.player_move_speed;
		done = False
		if (self._is_player_on_platform() == False):
			done = True
		next_state = self._return_state();
		return done, next_state;

	def _build_platforms(self):	# building the map.
		map_data = [0,1,2,1,0,0.5,1,0,-1,-2,-2,-2,-1,0,1,0,0,1,2,1,2,3,2,3];
		z = 0;
		for i in range(len(map_data)):
			x = map_data[i] * 0.6;
			z += 1;
			self.platforms.append(platform(x,z));

	def _is_player_on_platform(self):	# player dead or alive??
		for i in range(len(self.platforms)):
			platform = self.platforms[i];
			# sides of the platform
			plat_left = platform.x - self.platform_width/2;
			plat_right = platform.x + self.platform_width/2;
			plat_far = platform.z + self.platform_length/2;
			plat_close = platform.z - self.platform_length/2;
			# position of player
			px = self.player.x;
			pz = self.player.z;
			if ((px >= plat_left) and (px <= plat_right) and (pz <= plat_far) and (pz >= plat_close)):
				return True;
				break;
		return False;

	def _return_state(self):	# observation
		# player position and rotation as inputs
		p_x = self.player.x;
		p_z = self.player.z;
		p_r = self.player.r;
		# data normalization
		p_z /= 10;
		p_x /= 2;
		p_x += 0.5;
		print(p_x, p_z, p_r)
		return p_x, p_z, p_r;

	def _show_platforms(self):	# visualizing the map.
		print("showing platforms...")
		fig, ax = plt.subplots()
		for i in range(len(self.platforms)):
			platform = self.platforms[i];
			x,y = platform.x, platform.z;
			verts = [
			   (x-self.platform_width/2, y-self.platform_length/2),  # left, bottom
			   (x-self.platform_width/2, y+self.platform_length/2),  # left, top
			   (x+self.platform_width/2, y+self.platform_length/2),  # right, top
			   (x+self.platform_width/2, y-self.platform_length/2),  # right, bottom
			   (0., 0.),  # ignored
			]
			codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
			path = Path(verts, codes)
			patch = patches.PathPatch(path, facecolor='orange', lw=1)
			ax.add_patch(patch)
		ax.set_xlim(-18, 18)
		ax.set_ylim(0, 36)
		plt.show();
		print("done showing platforms.");
