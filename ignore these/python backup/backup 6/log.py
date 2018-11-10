# data visualization
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

class logger:
	def __init__(self):
		self.total_reward = 0;
		self.total_reward_list = [];

	def _show_graph(self):
		width = self.total_reward_list;
		plt.plot([0,len(width)], [0,0])
		x = list(range(0,len(width)))
		plt.scatter(x,width, color='k', s=10)
		plt.title("Game analysis")
		plt.xlabel("Episode")
		plt.ylabel("Rewards")
		plt.show();

	def _ep_recap(self, AI, env, complete): # episode recap
		# format to double digit
		log_color = "\033[92m" if complete else "\033[93m"
		eps = AI.episode
		rew = "%02d" % round(self.total_reward,2)
		ste = "%02d" % env.step
		PZ = "%02d" % round(env.player.z,2)
		eps = round(AI.epsilon, 2)
		# print
		print(f"{log_color}Episode: {eps}, cumulative reward: {rew}, steps: {ste}, pz: {PZ} epsilon: {eps}\033[0m")
		if AI.episode % 5 == 0:
			average_rew = round(sum(self.total_reward_list[-5:])/5,2);
			print(f"\033[94mAverage cumulative reward: {average_rew}\033[0m")
		# update variables
		self.total_reward_list.append(self.total_reward);
		self.total_reward = 0;

	def _show_platforms(self, env):	# visualizing the map.
		print("showing platforms...")
		fig, ax = plt.subplots()
		for i in range(len(env.platforms)):
			platform = env.platforms[i];
			x,y = platform.x, platform.z;
			verts = [
			   (x-env.platform_width/2, y-env.platform_length/2),  # left, bottom
			   (x-env.platform_width/2, y+env.platform_length/2),  # left, top
			   (x+env.platform_width/2, y+env.platform_length/2),  # right, top
			   (x+env.platform_width/2, y-env.platform_length/2),  # right, bottom
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