import matplotlib.pyplot as plt

x = [1,2,3,5,6,7]
y = [2,3,5,6,6,7];
plt.scatter(x,y, color='k')


plt.title("Game analysis")
plt.xlabel("Episode")
plt.ylabel("Rewards")
plt.show()