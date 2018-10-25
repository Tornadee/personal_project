				# © Jason (Seojoon) Yeon 
				# 2018 October 17 ~
# statistical
import random
import math
import numpy as np
# AI
from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers import Dense, Dropout
# visualization
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
# export
import tensorflowjs as tfjs

class AI:
	def __init__(self):
		self.num_states = 3;	# coordinates of player, rotation of player
		self.num_actions = 3;	# turn left, turn right, or go straight
		self.batch_size = 32;
		self.data = [];
		self.memory = 90000;
		self.episode = 0;
		self.max_episodes = 90;
		self.alpha = 0.001;		# learning rate
		self.gamma = 0.99;		# discount factor
		self.epsilon = 1.00;
		self.ep_decay = 0.999;
		self.min_ep = 0.1;
		self.model = self._create_model();
		self.total_reward = 0;
	
	def _create_model(self):
		model = Sequential();
		model.add(Dense(24, input_dim=self.num_states, activation="relu"))
		model.add(Dense(50, activation="relu"))
		model.add(Dense(self.num_actions, activation="linear"))#softmax / linear / sigmoid
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

	def _replay(self):				# Q-learning
		sample = random.sample(self.data, self.batch_size)
		for state, action, next_state, reward, done in sample:
			target = reward
			if done == False:
				nextPred = self.model.predict(np.array([next_state]))[0];
				target = reward + self.gamma * np.amax(nextPred)

			new_q = self.model.predict(np.array([state]))[0];
			index = action + 1;
			new_q[index] = target;
			print(f"{new_q} ==> {new_q[index]}");
			xss = np.array([state]) # input
			yss = np.array([new_q]) # Q-table output. Use Argmax to find the best action.
			self.model.fit(xss, yss, epochs=1, verbose=0)

	def _remember(self, data):		# store data
		self.data.append(data);
		if (len(self.data)) > self.memory:
			self.data.pop(0);

	def _save_model(self):			# export keras model
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
		self.player = player();
		self.player_move_speed = 0.4;
		self.player_steer_speed = 0.05;
		self.platform_width = 2.5;
		self.platform_length = 1;
		self.step = 0;
		self._build_platforms();
		#self._show_platforms();

	def _recap(self):			# summary of training results. Doesn't matter.
		print(f"\033[92mEpisode: {AI.episode}, cumulative reward: {round(AI.total_reward,2)}, steps: {self.step}, pz: {round(self.player.z,2)}\033[0m")
		AI.episode += 1;
		if AI.episode % 10 == 0:
			summation = 0;
			print(f"\033[94mEpsilon: {round(AI.epsilon, 2)}\033[0m")

	def _reset(self):			# reset environment and variables
		self.player.x, self.player.z, self.player.r = 0.0, 0.0, 0.0;
		self.step = 0;
		AI.total_reward = 0;

	def _move_player(self):		# apply action and return dead or alive
		self.player.x += math.sin(self.player.r) * self.player_move_speed;
		self.player.z += math.cos(self.player.r) * self.player_move_speed;
		if (self._is_player_on_platform() == False):
			return True; # done = True. (game over)
		else:
			return False;

	def _build_platforms(self):	# building the map.
		num_platforms = 0; # make 35 platforms.
		prev_z = -2;
		prev_x = 0;
		while num_platforms < 35:
			num_platforms += 1;
			shift_x = (random.randint(0, 1)-0.5) * 1.1;
			shift_z = self.platform_length;
			x = round(prev_x + shift_x, 1);
			z = round(prev_z + shift_z, 1);
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
		a = False; # is touching at least one platform
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
				a = True;
				break;
		return a;

	def _return_state(self):	# observation
		for i in range(len(self.platforms)):
			platform = self.platforms[i];
			if (platform.z > self.player.z + 1):
				# player position and rotation as inputs
				p_x = self.player.x;
				p_z = self.player.z;
				p_r = self.player.r;
				# data normalization
				p_z /= 36;
				p_x /= 36;
				return p_x, p_z, p_r;
		print("ERROR ERROR R!");

if __name__ == "__main__":
	AI = AI();		# agent
	game = game();	# environment
	state = game._return_state();
	# main loop
	while AI.episode < AI.max_episodes:
		# choose action either by random or by prediction.
		action = AI._choose_action(state);
		# apply the action
		game.player.r += action * game.player_steer_speed;
		# check if player is dead or alive
		done = game._move_player();
		# observe
		next_state = game._return_state();
		# reward structure
		reward = 1 if not done else -10
		'''if game.player.z >= 20:
			reward += 10
		elif game.player.z >= 10:
			reward += 5'''
		# save data
		AI._remember([state, action, next_state, reward, done])
		game.step += 1;
		if (len(AI.data) >= AI.batch_size):
			AI._replay();
		# pass on the state
		state = next_state;
		# epsilon effect
		if (len(AI.data) > AI.batch_size):
			if (AI.epsilon > AI.min_ep):
				AI.epsilon *= AI.ep_decay;
		# recap logging / seeing results
		AI.total_reward += reward;
		if done:
			game._recap();
			game._reset();
	
	# export model
	if False:
		AI._save_model();
		print("Below is the randomly generated map that the AI interacted in.");
		for i in range(len(game.platforms)):
			platform = game.platforms[i];
			print(f"x:{platform.x},z:{platform.z},");

