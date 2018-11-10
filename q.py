# © Jason (Seojoon) Yeon 2018 October 17 ~
# statistical
import random
import math
import numpy as np
# import game environment and logging tool
import env
import log
# machine learning
from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.models import load_model
import tensorflowjs as tfjs

class AI:
	def __init__(self):
		self.num_states = 6		# player x & z & rotation, nearest 3 blocks position x differences.
		self.num_actions = 3	# turn left, turn right, or go straight
		self.batch_size = 32
		self.data = []
		self.memory = 90000
		self.episode = 0
		self.max_episodes = 350
		self.alpha = 0.005		# learning rate   # so far best= 0.005
		self.gamma = 0.85		# discount factor # so far best= 0.85
		self.epsilon = 1.00
		self.ep_decay = 0.999
		self.min_ep = 0.1
		self.model = self._create_model()
	
	def _create_model(self):
		model = Sequential()
		model.add(Dense(24, input_dim=self.num_states, activation="relu"))
		model.add(Dense(48, activation="relu"))
		model.add(Dense(self.num_actions, activation="linear"))#softmax / linear / sigmoid
		adam = Adam(lr=self.alpha)
		model.compile(loss="mean_squared_error", optimizer=adam)
		return model

	def _choose_action(self, state):
		if (random.random() <= self.epsilon):
			action = math.floor(random.random() * self.num_actions) - 1
			if self.episode % 5 == 0:
				with open('read.txt', 'a') as the_file:
				    the_file.write(f'@a${action}')
			return action
		else:
			pred = self.model.predict(np.array([state]))[0]
			action = np.argmax(pred) - 1
			if self.episode % 5 == 0:
				with open('read.txt', 'a') as the_file:
				    the_file.write(f'@{pred}${action}')
			return action

	def _replay(self):				# Q-learning
		sample = random.sample(self.data, self.batch_size)
		for state, action, next_state, reward, done in sample:
			target = reward
			if done == False:
				nextPred = self.model.predict(np.array([next_state]))[0]
				target = reward + self.gamma * np.amax(nextPred)

			new_q = self.model.predict(np.array([state]))[0]
			index = action + 1
			new_q[index] = target
			#print(f"{new_q} ==> {new_q[index]}")
			xss = np.array([state]) # input
			yss = np.array([new_q]) # Q-table output. Use Argmax to find the best action.
			self.model.fit(xss, yss, epochs=1, verbose=0)

	def _remember(self, data):				# store data
		self.data.append(data)
		if (len(self.data)) > self.memory:
			self.data.pop(0)

	def _save_model(self, lastest_tot_rews):	# save h5 model
		# judge fitness
		if True: #103 in lastest_tot_rews
			self.model.save("my_model_1.h5")
			self.model.save("Keras-64x2-10epoch");
			tfjs.converters.save_keras_model(self.model, "tfjsmodel");
			print("model saved")
		else:
			print("model is unfit. Not saved.")
		# save model
		AI.model.save("my_model_1.h5")

if __name__ == "__main__":
	AI = AI()				# agent
	env = env.game()		# environment
	log = log.logger()		# data visualization

	state = env._return_state()
	# main loop
	while AI.episode < AI.max_episodes:
		action = AI._choose_action(state)
		done, next_state = env._step(action)
		# reward structure
		reward = 1 if not done else -90	# death penalty
		complete = (env.player.z >= env.platforms[-3].z)
		if complete:					# map completion bonus
			done = True
			reward = 20
			complete = True
			AI.min_ep = 0.05;

		# remember data
		AI._remember([state, action, next_state, reward, done])
		# replay
		if (len(AI.data) >= AI.batch_size):
			AI._replay()

		# epsilon decay
		if (len(AI.data) > AI.batch_size):
			if (AI.epsilon > AI.min_ep):
				AI.epsilon *= AI.ep_decay

		# recap logging to visualize results
		log.total_reward += reward
		if done:
			AI.episode += 1
			log._ep_recap(AI, env, complete)
			env._reset()

		# pass on the state to next iteration
		state = next_state

	log._show_platforms(env)
	log._show_graph()
	AI._save_model(log.total_reward_list[-6:-1])


