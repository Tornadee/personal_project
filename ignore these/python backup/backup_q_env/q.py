				# © Jason (Seojoon) Yeon 
				# 2018 October 17 ~
# statistical
import random
import math
import numpy as np
# game environment
import env
# machine learning
from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.models import load_model
# data visualization
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
# export model
#import tensorflowjs as tfjs

class AI:
	def __init__(self):
		self.num_states = 3;	# coordinates of player, rotation of player
		self.num_actions = 3;	# turn left, turn right, or go straight
		self.batch_size = 32;
		self.data = [];
		self.memory = 90000;
		self.episode = 0;
		self.max_episodes = 300;
		self.alpha = 0.01;		# learning rate   # so far best= 0.005
		self.gamma = 0.85;		# discount factor # so far best= 0.85
		self.epsilon = 1.00;
		self.ep_decay = 0.998;
		self.min_ep = 0.1;
		self.model = self._create_model();
		self.total_reward = 0;
		self.total_reward_list = [];
	
	def _create_model(self):
		model = Sequential();
		model.add(Dense(24, input_dim=self.num_states, activation="relu"))
		model.add(Dense(48, activation="relu"))
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
			#print(f"{new_q} ==> {new_q[index]}");
			xss = np.array([state]) # input
			yss = np.array([new_q]) # Q-table output. Use Argmax to find the best action.
			self.model.fit(xss, yss, epochs=1, verbose=0)

	def _remember(self, data):		# store data
		self.data.append(data);
		if (len(self.data)) > self.memory:
			self.data.pop(0);

	def _recap(self):				# summary of training results. Doesn't matter.
		print(f"\033[92mEpisode: {self.episode + 1}, cumulative reward: {round(self.total_reward,2)}, steps: {env.step}, pz: {round(env.player.z,2)}\033[0m")
		self.episode += 1;
		if self.episode % 10 == 0:
			print(f"\033[94mEpsilon: {round(self.epsilon, 2)}\033[0m")

	def _save_model(self):			# export keras model
		print("saving the model...")
		self.model.save("Keras-64x2-10epoch");
		tfjs.converters.save_keras_model(self.model, "tfjsmodel")

	def _show_graph(self):
		x = list(range(0,len(self.total_reward_list)))
		plt.scatter(x,self.total_reward_list, color='k', s=40)
		plt.title("Game analysis")
		plt.xlabel("Episode")
		plt.ylabel("Rewards")
		plt.show();

if __name__ == "__main__":
	AI = AI();		# agent
	env = env.game();	# environment
	state = env._return_state();
	# main loop
	while AI.episode < AI.max_episodes:
		action = AI._choose_action(state);
		done, next_state = env._step(action);
		# reward structure
		reward = 1 if not done else -20
		# remember data
		AI._remember([state, action, next_state, reward, done])
		# replay
		if (len(AI.data) >= AI.batch_size):
			AI._replay();
		# epsilon effect
		if (len(AI.data) > AI.batch_size):
			if (AI.epsilon > AI.min_ep):
				AI.epsilon *= AI.ep_decay;
		# recap logging / seeing results
		AI.total_reward += reward;
		if done:
			AI._recap();
			env._reset();
			AI.total_reward_list.append(AI.total_reward);
			AI.total_reward = 0;
		# pass on the state
		state = next_state;

	#env._show_platforms();
	AI._show_graph();
	# save model
	'''
	save_threshold = -8; # lower number = save more.
	if AI.total_reward_list[-1] > save_threshold:
		AI.model.save("my_model_1.h5");
	elif AI.total_reward_list[-2] > save_threshold:
		AI.model.save("my_model_1.h5");
	elif AI.total_reward_list[-3] > save_threshold:
		AI.model.save("my_model_1.h5");
	else:
		print(f"{AI.total_reward_list[-1]} only. Model is not fit enough.");'''


