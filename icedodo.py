from threading import Timer
import random
import math
import keras

class AI:
	def __init__(self):
		self.num_states = 5;
		self.num_actions = 3;

		self.alpha = 0.01;
		self.epsilon = 1.00;
		self.ep_decay = 0.994;
		self.model = _create_model();
	
	def _create_model(self):
		model = Sequential();
		return model;

	def _choose_action(self, data):
		if (random.random() <= self.epsilon):

		else:
			prediction = _argmax_predict(data);

	def _argmax_predict(self, data)
		pred = self.model.predict(data);
		return pred # argmax this.

	def _predict(self, data)
		pred = self.model.predict(data);
		return pred


class player:
	def __init__(self):
		self.x, self.z, self.r = 0.0, 0.0, 0.0;

class platform:
	def __init__(self, x, z):
		self.x, self.z = x, z;

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
			if (self.frame % 1000) == 0:
				print("survived frame {}".format(self.frame));
			self._update();

	def _update(self):
		while (self.player.z + 20 >= self.previous_platform_z):
			self._build_platform()
		if (self.platforms[0].z) < self.player.z - 2.6:
			self.platforms.pop(0);

		# this part will be controlled by the AI.
		a_x, a_z, b_x, b_z = self._get_upcoming_blocks_pos();
		data = (self.player.x, self.player.z, a_x, a_z, b_x, b_z);
		action = AI._choose_action(data);
		self.player.r += action;
		self._move_player();

	def _move_player(self):
		self.player.x += math.sin(self.player.r) * 0.4;
		self.player.z += math.cos(self.player.r) * 0.4;
		if (self._is_player_on_platform() == False):
			self.alive = False;
			print("score: {}".format(str(round(self.player.z))));

	def _build_platform(self):
		shift_x = random.randint(-1,1);
		shift_z = 5;
		x = self.previous_platform_x + shift_x;
		z = self.previous_platform_z + shift_z;
		self.platforms.append(platform(x,z));

		# next platform will be placed based on this relative position
		self.previous_platform_x = x;
		self.previous_platform_z = z;

	def _is_player_on_platform(self):
		a = False; # is touching at least one platform
		for i in range(len(self.platforms)):
			platform = self.platforms[i];
			# sides of the platform
			plat_left = platform.x - 1;
			plat_right = platform.x + 1;
			plat_far = platform.z + 2.5;
			plat_close = platform.z - 2.5;
			# position of player
			px = self.player.x;
			pz = self.player.z;
			withinBounds = ((px > plat_left) and (px < plat_right) and (pz < plat_far) and (pz > plat_close));
			if withinBounds:
				a = True;
				break;
		return a;

	def _get_upcoming_blocks_pos(self):
		a_x, a_z, b_x, b_z = 0,0,0,0;
		a_index = None;
		for i in range(len(self.platforms)):
			platform = self.platforms[i];
			if (platform.z > self.player.z + 1):
				a_index = 
		
		return a_x, a_z, b_x, b_z;

if __name__ == "__main__":
	game = game();
