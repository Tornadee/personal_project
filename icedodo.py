# © Jason (Seojoon) Yeon 
# 2018 October 17 ~ 

import random
import math
import numpy as np
from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers import Dense, Dropout

class AI:
	def __init__(self):
		self.num_states = 6; # px, pz, ax, az, bx, bz
		self.num_actions = 3; # -1 or 0 or 1
		self.batch_size = 32;
		self.data = [];
		self.memory = 50000;

		self.alpha = 0.01;
		self.gamma = 0.99;
		self.epsilon = 1.00;
		self.ep_decay = 0.994;
		self.min_ep = 0.02;
		self.model = self._create_model();
	
	def _create_model(self):
		model = Sequential();
		model.add(Dense(24, input_shape=(self.num_states,), activation="relu"))
		model.add(Dense(24, activation="relu"))
		model.add(Dense(self.num_actions, activation="linear"))
		adam = Adam(lr=self.alpha);
		model.compile(adam, loss="mean_squared_error");
		return model;

	def _choose_action(self, state):
		if (random.random() <= self.epsilon):
			return (random.random() * self.num_actions) - 1;
		else:
			pred = self.model.predict(np.array([state]))[0];
			arg_max = np.argmax(pred);
			return arg_max

	def _replay(self):
		sample = self._sample(self.data, self.batch_size);
		for state, action, next_state, reward, done in sample:
			# new Q-table = 
			# Current Q-table +
			q_current = self.model.predict(np.array([state]));
			# discount rate (gamma) * max_possible Q
			q_future = self.model.predict(np.array([next_state]))[0];
			max_q = q_future[np.argmax(q_future)];
			# new Q_s_a =
			q_new = q_current + self.alpha * (reward + (self.gamma * max_q) - q_current)
			# assignment
			q_current[action] = q_new
			xs = np.array()
			ys = np.array()
			self.model.fit(xs, ys, epochs=1);

	def _predict(self, state):
	    pred = self.model.predict(np.array(state));
	    return pred;


	def _sample(self, data, count):
		if (count > len(data)):
			return False;
		else:
			sample = [];
			sampled_ids = [];
			while len(sample) < count:
				rand_id = random.randint(0, count-1);
				if rand_id not in sampled_ids:
					sample.append(data[rand_id]);
					sampled_ids.append(rand_id);
			return sample;

	def _add_to_memory(self, data):
		self.data.append(data);
		if (len(self.data)) > self.memory:
			self.data.pop(0);

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
		self.state = self._return_state();

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
		action = AI._choose_action(self.state);
		self.player.r += action;
		# data collection part
		done = self._move_player();
		next_state = self._return_state();
		# Q-learning
		reward = 1 if not done else -10
		AI._add_to_memory([self.state, action, next_state, reward, done])
		if (len(AI.data) >= AI.batch_size):
			AI._replay();
		# pass on the state
		self.state = next_state;
		# epsilon effect
		if (len(AI.data) > AI.batch_size):
			if (AI.epsilon > AI.min_ep):
				AI.epsilon *= AI.ep_decay;

	def _move_player(self):
		self.player.x += math.sin(self.player.r) * 0.4;
		self.player.z += math.cos(self.player.r) * 0.4;
		if (self._is_player_on_platform() == False):
			self.alive = False;
			print("score: {}".format(str(round(self.player.z))));
			return True;
		else:
			return False;

	def _build_platform(self):
		shift_x = random.randint(-0,0);
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

	def _return_state(self):
		a_index = None;
		for i in range(len(self.platforms)):
			platform = self.platforms[i];
			if (platform.z > self.player.z + 1):
				# player position
				p_x = self.player.x;
				p_z = self.player.z;
				# closest next platform, called "a"
				a_x = platform.x;
				a_z = platform.z;
				# second next platform, called "b"
				b_x = self.platforms[i+1].x;
				b_z = self.platforms[i+1].z;
				a_index = i;
				return p_x, p_z, a_x, a_z, b_x, b_z;

if __name__ == "__main__":
	AI = AI();
	game = game();
