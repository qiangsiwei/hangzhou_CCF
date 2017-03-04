# -*- coding: utf-8 -*- 

import glob
import math
import fileinput
import numpy as np
from pylab import *

# 时间粒度为1小时
# 空间粒度为500米
# 20-24为工作日

ranget, rangex, rangey = 24, 90, 60

def euclidean(p1,p2):
	dist = math.sqrt(sum([pow(i-j,2) for i,j in zip(p1,p2)]))
	return dist

def statistic_L_function():
	from scipy import interpolate

	fig = plt.figure(figsize=(8,5))
	ax1 = fig.add_subplot(111)

	wds, wes = ['0820','0821','0822','0823','0824'], ['0819','0825','0826']
	for flist, linestyle, label in [(wds,'k-',"Weekday"),(wes,'k--',"Weekend")]:
		mesh = [[0 for j in xrange(rangey)] for i in xrange(rangex)]
		for filename in sorted(glob.glob(r"../data/pos_user#/*")):
			if filename.split("/")[-1] in ["{0}.txt".format(fname) for fname in flist]:
				for line in fileinput.input(filename):
					part = line.strip().split(" ")
					px, py, n = int(part[0].split(",")[0]), int(part[0].split(",")[1]), int(part[1])
					mesh[px][py] += n
				fileinput.close()

		plist = sorted([mesh[i][j] for i in xrange(rangex) for j in xrange(rangey)], reverse=True)[0:1000]
		itemlist = sorted([{"p":[i,j],"v":mesh[i][j]} for i in xrange(rangex) for j in xrange(rangey)], key=lambda x:x["v"], reverse=True)[0:500]
		prodlist = [0 for i in xrange(30)]
		for i in xrange(500):
			for j in xrange(500):
				dist, prod = euclidean(itemlist[i]["p"],itemlist[j]["p"]), itemlist[i]["v"]*itemlist[j]["v"]
				if i != j and dist < 30:
					prodlist[min(int(dist),29)] += prod
		prodlist_sum = sum(prodlist)
		for i in range(len(prodlist)-1,-1,-1):
			prodlist[i] = (math.sqrt((math.pi*30**2)*sum(prodlist[0:i+1])/prodlist_sum/math.pi)-i)*500
	
		tck = interpolate.splrep([i*500 for i in xrange(30)][1:],prodlist[1:],s=0)
		x = np.arange(500,13000,100)
		y = interpolate.splev(x,tck,der=0)
		plt.plot(x,y,linestyle,label=label,linewidth=2)

	plt.xlim(0,14000)
	plt.ylim(0,7000)
	plt.xlabel('Distance /m')
	plt.ylabel('L(d)')
	handles, labels = ax1.get_legend_handles_labels()
	ax1.legend(handles,labels)
	subplots_adjust(wspace=0.4,hspace=0.4)
	# show()
	for postfix in ('eps','png'):
		savefig('../figure/{0}/04.{0}'.format(postfix))


if __name__ == "__main__":
	statistic_L_function()

