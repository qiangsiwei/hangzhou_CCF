# -*- coding: utf-8 -*- 

import glob
import fileinput
import numpy as np
from pylab import *

# 时间粒度为1小时
# 空间粒度为200米
# 20-24为工作日

ranget, rangex, rangey = 24, 225, 150

def demonstrate_tide_effect():
	day = [[[[0]*ranget for j in xrange(rangey)] for i in xrange(rangex)] for d in xrange(8)]
	for d, filename in enumerate(sorted(glob.glob(r"../data/pos_hour_user#/*"))):
		print filename
		for line in fileinput.input(filename):
			part = line.strip().split(" ")
			px, py, s, c = int(part[0].split(",")[0]), int(part[0].split(",")[1]), int(part[1]), int(part[2])
			day[d][px][py][s] = c
		fileinput.close()

	for dlist, fname in [(range(1,6),"weekday"),(range(0,1)+range(6,8),"weekend")]:
		mask = np.array([[1 if np.array([[day[df][i][j][kf] for kf in xrange(ranget)] for df in dlist]).sum()/len(dlist)>=10*ranget else 0 \
					for j in xrange(rangey)] for i in xrange(rangex)]).sum()
		mesh = [[[sum([day[d][i][j][k] for d in dlist])/len(dlist) if np.array([[day[df][i][j][kf] for kf in xrange(ranget)] for df in dlist]).sum()/len(dlist)>=10*ranget else 0 for k in xrange(ranget)] \
					for j in xrange(rangey)] for i in xrange(rangex)]
		mesh = [[[float(mesh[i][j][k])/sum(mesh[i][j]) if sum(mesh[i][j])!=0 else 0 for k in xrange(ranget)] \
					for j in xrange(rangey)] for i in xrange(rangex)]
		avg = [float(np.array([[mesh[i][j][k] for j in xrange(rangey)] for i in xrange(rangex)]).sum())/mask for k in xrange(ranget)]
		mesh = [[[mesh[i][j][k]-avg[k] if sum(mesh[i][j])!=0 else 0 for k in xrange(ranget)] \
					for j in xrange(rangey)] for i in xrange(rangex)]
		with open("../data/var/{0}.txt".format(fname),"w") as f:
			for i in xrange(rangex):
				for j in xrange(rangey):
					if sum(mesh[i][j])!=0:
						f.write("{0} {1} {2}\n".format(i,j," ".join([str(round(x,6)) for x in mesh[i][j]])))

	plt.figure(figsize=(12,8))
	levels = arange(-1, 1.1, 0.1) 
	cmap, norm = cm.PRGn, cm.colors.Normalize(vmax=1.1, vmin=-1)
	for c, t in enumerate([4,8,10,16,18,22]):
		colormap = [[0 for j in xrange(rangey)] for i in xrange(rangex)]
		for line in fileinput.input("../data/var/weekday.txt"):
			part = line.strip().split(" ")
			x, y, f = int(part[0]), int(part[1]), float(part[2:][t])
			colormap[x][y] = f
		fileinput.close()
		cmax = np.array([[abs(colormap[i][j]) for j in xrange(rangey)] for i in xrange(rangex)]).max()
		colormap = [[colormap[i][j]/cmax for j in xrange(rangey)] for i in xrange(rangex)]
		(X, Y), C = meshgrid(np.arange(100), np.arange(100)), np.array(colormap)[20:120,20:120]
		subplot(2,3,c+1)
		cset = contourf(X, Y, C.T, levels, cmap=cm.get_cmap("seismic", len(levels)), norm=norm)
		plt.axis([0, 100-1, 0, 100-1])
		plt.xticks(np.linspace(0,100,6))
		plt.yticks(np.linspace(0,100,6))
		plt.title('{0}:00'.format(str(t).zfill(2)))
		if c == 0:
			plt.xlabel('Longitude grid index /200m')
			plt.ylabel('Latitude grid index /200m')
		if c == 3:
			subplots_adjust(hspace=0.4)
	subplots_adjust(bottom=0.1, left=0.06, right=0.9, top=0.9)
	cax2 = axes([0.92, 0.10, 0.01, 0.8])
	colorbar(cax=cax2)
	# show()
	for postfix in ('eps','png'):
		savefig('../figure/{0}/11.{0}'.format(postfix))


if __name__ == "__main__":
	demonstrate_tide_effect()

