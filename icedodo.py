from threading import Timer
import random
import math

class player:
	def __init__(self):
		self.x, self.z, self.r = 0.0, 0.0, 0.0;

class game:
	def __init__(self):
		self.platforms = [];
		self.previous_platform_x = 0;
		self.previous_platform_z = -5;
		self.player = player();
		self.alive = True;
		self.frame = 0;
		while self.alive:
			self.frame += 1;
			'''if (self.frame % 100) == 0:
				#print("survived frame {}".format(self.frame));
				print("{}, {}".format(self.player.x, self.player.z));'''
			self._update();

	def _update(self):
		while (self.player.z + 20 >= self.previous_platform_z):
			self._build_platform()

		action = random.random() - 0.5;
		self.player.r += action;
		self._move_player();

	def _move_player(self):
		self.player.x += math.sin(self.player.r) * 0.4;
		self.player.z += math.cos(self.player.r) * 0.4;
		#print("z: {} x {}".format(str(round(self.player.z)), str(round(self.player.x))));
		if (self._is_player_on_platform() == False):
			self.alive = False;
			print("score: {}".format(str(round(self.player.z))));

	def _build_platform(self):
		shift_x = random.randint(-0,0)
		shift_z = 5
		x = self.previous_platform_x + shift_x;
		z = self.previous_platform_z + shift_z;
		self.platforms.append([x,z]);

		# next platform will be placed based on this relative position
		self.previous_platform_x = x;
		self.previous_platform_z = z;

	def _is_player_on_platform(self):
		a = False; # is touching at least one platform
		for i in range(len(self.platforms)):
			platform = self.platforms[i];
			# sides of the platform
			plat_left = platform[0] - 1;
			plat_right = platform[0] + 1;
			plat_far = platform[1] + 2.5;
			plat_close = platform[1] - 2.5;
			# position of player
			px = self.player.x;
			pz = self.player.z;
			withinBounds = ((px > plat_left) and (px < plat_right) and (pz < plat_far) and (pz > plat_close));
			if withinBounds:
				a = True;
				break;
		return a;

if __name__ == "__main__":
	game = game();
