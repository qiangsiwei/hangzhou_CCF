# -*- coding: utf-8 -*- 

import fileinput
import numpy as np
from pylab import *
from constant import *

# 时间粒度为1小时
# 空间粒度为200米
# 20-24为工作日

ranget, rangex, rangey = 24, 225, 150

def statistic_density_base_station():
	mesh = [[0 for j in xrange(rangey)] for i in xrange(rangex)]
	for line in fileinput.input("../data/base_station/hz_base.txt"):
		part = line.strip().split(" ")
		lng, lat = float(part[3]), float(part[4])
		if lng_min<=lng<lng_max and lat_min<=lat<=lat_max:
			gx, gy = int((lng-lng_min)/(lng_max-lng_min)*rangex), int((lat-lat_min)/(lat_max-lat_min)*rangey)
			mesh[gx][gy]+=1
	fileinput.close()

	subplot(1,1,1)
	(X, Y), C = meshgrid(np.arange(rangex), np.arange(rangey)), np.array(mesh)
	cset1 = pcolormesh(X, Y, C.T, cmap=cm.get_cmap("OrRd"))
	colorbar(cset1)
	plt.axis([0, rangex-1, 0, rangey-1])
	plt.xlabel('Longitude grid index /200m')
	plt.ylabel('Latitude grid index /200m')
	# show()
	for postfix in ('eps','png'):
		savefig('../figure/{0}/01.{0}'.format(postfix))

if __name__ == "__main__":
	statistic_density_base_station()

