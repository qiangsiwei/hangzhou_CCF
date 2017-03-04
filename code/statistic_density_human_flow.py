# -*- coding: utf-8 -*- 

import glob
import fileinput
import numpy as np
from pylab import *

# 时间粒度为1小时
# 空间粒度为500米
# 20-24为工作日

ranget, rangex, rangey = 24, 90, 60

def statistic_density_human_flow():
	cut_off, scale = 80000, 5000
	mesh = [[0 for j in xrange(rangey)] for i in xrange(rangex)]
	for filename in sorted(glob.glob(r"../data/pos_user#/*")):
		print filename
		for line in fileinput.input(filename):
			part = line.strip().split(" ")
			px, py, n = int(part[0].split(",")[0]), int(part[0].split(",")[1]), int(part[1])
			mesh[px][py] += n
		fileinput.close()

	subplot(1,1,1)
	(X, Y), C = meshgrid(np.arange(rangex), np.arange(rangey)), np.array(mesh)
	levels, norm = arange(0, cut_off, scale), cm.colors.Normalize(vmax=cut_off, vmin=0)
	cset1 = contourf(X, Y, C.T, levels, cmap=cm.get_cmap("OrRd", len(levels)), norm=norm)
	colorbar(cset1)
	plt.axis([0, rangex-1, 0, rangey-1])
	plt.xlabel('Longitude grid index /500m')
	plt.ylabel('Latitude grid index /500m')
	# show()
	for postfix in ('eps','png'):
		savefig('../figure/{0}/02.{0}'.format(postfix))


if __name__ == "__main__":
	statistic_density_human_flow()

