import random
import math

class player:
	def __init__(self):
		self.x, self.z, self.r = 0.0, 0.0, 0.0;

class platform:
	def __init__(self, x,z):
		self.x, self.z = x,z;
		self.width = 2
		self.length = 5

class game:
	def __init__(self):
		self.platforms = [];
		self.previous_platform_x = 0;
		self.previous_platform_z = 0;
		self.player = player();
		self.alive = True;
		while self.alive:
			self._update()

	def _update(self):
		action = 0;
		self.player.r += action;
		self._move_player();

	def _move_player(self):
		self.player.x += math.sin(self.player.r);
		self.player.z += math.cos(self.player.r);

	def _build_map(self):
		shift_x = random.randint(-3,3)
		shift_z = 5
		x = previous_platform_x + shift_x;
		z = previous_platform_z + shift_z;
		platforms.append(platform(x,z));

		# next platform will be placed based on this relative position
		previous_platform_x = x;
		previous_platform_z = z;

	def _is_player_on_platform(self):
		for i in range(len(self.platforms)):
			platform = self.platforms[i];
			if (platform.x + platform.width) > self.player.x:
				return False;
		return True;



if __name__ == "__main__":
	game = game();
