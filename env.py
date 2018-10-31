# statistical
import random
import math
import numpy as np

# visual
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
		self.player_move_speed = 0.4;
		self.player_steer_speed = 0.05;
		self.platform_width = 2.5;
		self.platform_length = 1;
		self.num_platforms = 35;
		self.step = 0;
		self._build_platforms();
		#self._show_platforms();

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
		map_data = [[0,0],[0.6,1],[1.1,2],[0.6,3],[0.0,4],[0.6,5],[0.0,6],[-0.6,7],[-1.1,8],[-0.6,9],[-0.0,10],[0.6,11],[0.0,12],[0.6,13],[0.0,14],[0.6,15],[1.1,16],[1.7,17],[1.1,18],[0.6,19],[1.1,20],[0.6,21],[1.1,22],[0.6,23],[0.0,24],[-0.6,25],[-1.1,26],[-0.6,27],[-1.1,28],[-0.6,29],[-1.1,30],[-1.7,31],[-1.1,32],[-1.7,33],[-2.2,34]];

		prev_z = -1;
		prev_x = 0;
		for i in range(self.num_platforms):
			'''shift_x = (random.randint(0, 1)-0.5) * 1.1;
			if i == 0:
				shift_x=0;
			shift_z = self.platform_length;
			x = round(prev_x + shift_x, 1);
			z = round(prev_z + shift_z, 1);'''
			x = map_data[i][0];
			z = map_data[i][1];
			self.platforms.append(platform(x,z));
			# next platform will be placed based on this relative position
			prev_x = x;
			prev_z = z;

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
		p_z /= 6;
		p_x /= 6;
		return p_x, p_z, p_r;
		'''
		for i in range(len(self.platforms)):
			platform = self.platforms[i]
			platform2 = self.platforms[i+1]
			if (platform.z >= self.player.z):
				dx = platform.x - self.player.x;
				dx /= 10;
				dx2 = platform.x - self.player.x;
				dx2 /= 10;
				pz = self.player.z;
				pz /= 100;
				pr = self.player.r
				return dx, dx2, pz, pr;
				break;'''
		print("ERROR ERROR R!");
