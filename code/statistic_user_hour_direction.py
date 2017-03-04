# -*- coding: utf-8 -*- 

import glob
import math
import fileinput

# 时间粒度为1小时
# 空间粒度为200米
# 20-24为工作日

ranget, rangex, rangey = 24*2, 225, 150

def euclidean(p1,p2):
	dist = math.sqrt(sum([pow(i-j,2) for i,j in zip(p1,p2)]))
	return dist
	
def statistic_user_hour_direction():
	direc_last = [[[[] for t in xrange(ranget)] for j in xrange(rangey)] for i in xrange(rangex)]
	direc_next = [[[[] for t in xrange(ranget)] for j in xrange(rangey)] for i in xrange(rangex)]
	for filename in sorted(glob.glob(r"../data/user_30min_center/*")):
		print filename
		user, lastt, lastx, lasty = "", -1, -1, -1
		for line in fileinput.input(filename):
			part = line.strip().split(" ")
			u, t, x, y = part[0], int(part[1]), int(float(part[2].split(",")[0])), int(float(part[2].split(",")[1]))
			if u == user and t == lastt+1 and (x != lastx or y != lasty):
				direc_last[x][y][t].append([lastx,lasty])
				direc_next[lastx][lasty][lastt].append([x,y])
			else:
				user, lastt, lastx, lasty = u, t, x, y
		fileinput.close()

	for fname, direc in [("last",direc_last),("next",direc_next)]:
		with open("../data/var/direction_{0}.txt".format(fname),"w") as f:
			for i in xrange(rangex):
				for j in xrange(rangey):
					_sum = sum([len(t) for t in direc[i][j]])
					if _sum >= 10*24*2:
						f.write("{0} {1} {2} {3}\n".format(i,j,_sum," ".join(["|".join(["{0},{1}".format(p[0]-i,p[1]-j) for p in t]) for t in direc[i][j]])))

def plot_user_hour_direction(picx, picy):
	from pylab import *
	from constant import *

	print 1.*picx/rangex*(lng_max-lng_min)+lng_min, 1.*picy/rangey*(lat_max-lat_min)+lat_min
	for line in fileinput.input("../data/var/direction_next.txt"):
		part = line.strip().split(" ")
		x, y, s, f = int(part[0]), int(part[1]), int(part[2]), [[[int(k) for k in j.split(",")] for j in i.split("|")] if len(i)!=0 else [] for i in part[3:]]
		if x == picx and y == picy:
			direcs = [[] for d in xrange(8)]
			for T in xrange(ranget-1):
				if len(f[T])!=0:
					for item in f[T]:
						angle = math.atan2(item[1],item[0])
						dist = euclidean(item,[0,0])
						if -math.pi/8 < angle <= math.pi/8:
							direcs[0].append(dist)
						elif math.pi/8 < angle <= math.pi*3/8:
							direcs[1].append(dist)
						elif math.pi*3/8 < angle <= math.pi*5/8:
							direcs[2].append(dist)
						elif math.pi*5/8 < angle <= math.pi*7/8:
							direcs[3].append(dist)
						elif math.pi*7/8 < angle <= math.pi or -math.pi <= angle <= -math.pi*7/8:
							direcs[4].append(dist)
						elif -math.pi*7/8 < angle <= -math.pi*5/8:
							direcs[5].append(dist)
						elif -math.pi*5/8 < angle <= -math.pi*3/8:
							direcs[6].append(dist)
						elif -math.pi*3/8 < angle <= -math.pi/8:
							direcs[7].append(dist)
			# width = [math.pi/2*len(direcs[i])/sum([len(direcs[j]) for j in xrange(8)]) for i in xrange(8)]
			radii = [int(200.0*sum(direcs[i])/len(direcs[i])) for i in xrange(8)]
			theta = [math.pi*i/4 for i in xrange(8)]
			ax = plt.subplot(111, polar=True)
			plt.ylim(0,2000)
			# plt.polar(theta,radii)
			plt.fill(theta,radii,"y",joinstyle='bevel',color='r',alpha=0.6)
			plt.show()


if __name__ == "__main__":
	# statistic_user_hour_direction()
	picx, picy = 38, 76
	# picx, picy = 68, 93
	# picx, picy = 123, 90
	# picx, picy = 74, 22
	# picx, picy = 71, 69
	plot_user_hour_direction(picx, picy)

