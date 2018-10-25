import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

def draw_platform(x,y):
	verts = [
	   (x-1.25, y-2.5),  # left, bottom
	   (x-1.25, y+2.5),  # left, top
	   (x+1.25, y+2.5),  # right, top
	   (x+1.25, y-2.5),  # right, bottom
	   (0., 0.),  # ignored
	]
	codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]

	path = Path(verts, codes)

	fig, ax = plt.subplots()
	patch = patches.PathPatch(path, facecolor='orange', lw=2)
	ax.add_patch(patch)
	ax.set_xlim(-100, 100)
	ax.set_ylim(0, 200)
	plt.show()

draw_platform(0,0);