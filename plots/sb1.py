import seaborn as sns
import numpy as np

fig = self._view_frame.figure

data = np.loadtxt(r'data.csv',delimiter=',')
ax = fig.add_subplot(111)
ax.cla()
sns.kdeplot(data, bw=10, kernel='gau',  cmap="Reds")
ax.scatter(data[:,0],data[:,1], color='r')

fig.canvas.draw()