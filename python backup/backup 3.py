# © Jason (Seojoon) Yeon 
# 2018 October 17 ~
import random
import math
import numpy as np
from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers import Dense, Dropout

import tensorflowjs as tfjs

class AI:
	def __init__(self):
		self.num_states = 2; # px, pz#, ax, az, bx, bz
		self.num_actions = 3; # -1 or 0 or 1
		self.batch_size = 32;
		self.data = [];
		self.memory = 50000;
		self.total_reward = 0;
		self.episode = 0;
		self.max_episodes = 80;
		self.rewards = [];

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
		model.compile(loss="mean_squared_error", optimizer=adam);
		return model;

	def _choose_action(self, state):
		if (random.random() <= self.epsilon):
			action = math.floor(random.random() * self.num_actions) - 1;
			return action
		else:
			pred = self.model.predict(np.array([state]))[0];
			action = np.argmax(pred) - 1;
			return action

	def _replay(self):
		sample = self._sample(self.data, self.batch_size);
		for state, action, next_state, reward, done in sample:
			target = reward
			if not done:
				# Q s-a
				next_state_prediction = self.model.predict(np.array([next_state]))[0];
				target = reward + self.gamma * np.amax(next_state_prediction)

			new_q = self.model.predict(np.array([state]))[0];
			new_q[action] = target
			xss = np.array([state]) # input
			yss = np.array([new_q]) # Q-table output. Use Argmax to find the best action.
			self.model.fit(xss, yss, epochs=1, verbose=0)

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

	def _remember(self, data):
		self.data.append(data);
		if (len(self.data)) > self.memory:
			self.data.pop(0);

	def _save_model(self):
		# this is the saving functions to export the weights of the model
		print("saving the model...")
		self.model.save("Keras-64x2-10epoch");
		tfjs.converters.save_keras_model(self.model, "tfjsmodel")

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
		self.player_move_speed = 0.4;
		self.player_steer_speed = 0.5;
		self.step = 0;
		self.deviation = 0.9;
		self._build_platforms();

	def _recap(self):
		print(f"\033[92mEpisode: {AI.episode}, cumulative reward: {AI.total_reward}, steps: {self.step}\033[0m")
		AI.episode += 1;
		AI.rewards.append(AI.total_reward);
		if AI.episode % 10 == 0:
			summation = 0;
			for i in range(AI.episode - 10, AI.episode - 1):
				summation += AI.rewards[i];
			recap = summation / 10;
			print(f"\033[94mPrevious 10 episodes: Average total reward: {recap}, Epsilon: {round(AI.epsilon, 2)}\033[0m")

	def _reset(self): # reset environment
		# randomize map or keep the same map?
		'''
		self.platforms = [];
		self.previous_platform_x = 0;
		self.previous_platform_z = -5;
		self._build_platforms();'''
		self.player.x, self.player.z, self.player.r = 0.0, 0.0, 0.0;
		self.step = 0;
		AI.total_reward = 0;

	def _move_player(self):
		self.player.x += math.sin(self.player.r) * self.player_move_speed;
		self.player.z += math.cos(self.player.r) * self.player_move_speed;
		# done?
		if (self._is_player_on_platform() == False):
			return True;
		else:
			return False;

	def _build_platforms(self):
		# build platforms ahead
		num_platforms = 0; # make 300 platforms.
		while num_platforms < 300:
			num_platforms += 1;
			shift_x = random.randint(-1, 1) * self.deviation;
			shift_z = 5;
			x = self.previous_platform_x + shift_x;
			z = self.previous_platform_z + shift_z;
			self.platforms.append(platform(x,z));
			# next platform will be placed based on this relative position
			self.previous_platform_x = x;
			self.previous_platform_z = z - 0.5;
		# clean up past platforms
		if (self.platforms[0].z) < self.player.z - 2.6:
			self.platforms.pop(0);

	def _is_player_on_platform(self):
		a = False; # is touching at least one platform
		for i in range(len(self.platforms)):
			platform = self.platforms[i];
			# sides of the platform
			plat_left = platform.x - 1.25;
			plat_right = platform.x + 1.25;
			plat_far = platform.z + 2.5;
			plat_close = platform.z - 2.5;
			# position of player
			px = self.player.x;
			pz = self.player.z;
			withinBounds = ((px > plat_left) and (px < plat_right) and (pz < plat_far) and (pz > plat_close));
			#print(f"i={i}")
			#print(f"left={plat_left}, right={plat_right}, far={plat_far}, close={plat_close}");
			#print(f"px={self.player.x}, pz={self.player.z}, withinBound={withinBounds}");
			if withinBounds:
				a = True;
				break;
		return a;

	def _return_state(self):
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
				return p_x, p_z#, a_x, a_z, b_x, b_z;
		print("WARNING RETURNING STATE WARNING WARNING WARNING WARNING WARNING WARNING WARNING WARNING WARNING")
		return None

if __name__ == "__main__":
	AI = AI();		# agent
	game = game();	# environment
	state = game._return_state();
	while AI.episode < AI.max_episodes:
		# this part will be controlled by the AI.
		action = AI._choose_action(state);
		game.player.r += action * game.player_steer_speed;
		# data collection part
		done = game._move_player();
		next_state = game._return_state();
		# Q-learning
		reward = 1 if not done else -200
		AI.total_reward += reward;
		AI._remember([state, action, next_state, reward, done])
		game.step += 1;
		print(f"Step {game.step}, x={round(game.player.x, 2)}, z={round(game.player.z, 2)}, r={round(game.player.r, 2)}, action={action}");
		if (len(AI.data) >= AI.batch_size):
			AI._replay();
		# pass on the state
		state = next_state;
		# epsilon effect
		if (len(AI.data) > AI.batch_size):
			if (AI.epsilon > AI.min_ep):
				AI.epsilon *= AI.ep_decay;
		# recap logging
		if done:
			game._recap();
			game._reset();
	# finished training. Now export to tensorflow js.
	AI._save_model();
	for i in range(len(game.platforms)):
		platform = game.platforms[i];
		print(f"x={platform.x},z={platform.z}");

