# -*- coding: utf-8 -*- 

import glob
import fileinput
import numpy as np
from pylab import *

# 时间粒度为1小时
# 空间粒度为200米
# 20-24为工作日

ranget, rangex, rangey = 24, 225, 150

def statistic_hour_user():
	d, day = 0, [[0 for j in xrange(ranget)] for i in xrange(8)]
	for filename in sorted(glob.glob(r"../data/hour_user#/*")):
		print filename
		for line in fileinput.input(filename):
			part = line.strip().split(" ")
			t, n = int(part[0]), int(part[1])
			day[d][t] = n
		fileinput.close()
		d += 1
	wd, we = [day[1],day[2],day[3],day[4],day[5]],[day[0],day[6],day[7]]
	wd_avg = [np.average([wd[d][t] for d in xrange(5)])/10**4 for t in xrange(ranget)]
	we_avg = [np.average([we[d][t] for d in xrange(3)])/10**4 for t in xrange(ranget)]
	
	from scipy import interpolate
	from matplotlib.ticker import MultipleLocator, FormatStrFormatter
	fig = plt.figure(figsize=(8,5))
	ax = fig.add_subplot(111)
	for data, linestyle, label in [(wd_avg,'k-',"Weekday"),(we_avg,'k--',"Weekend")]:
		tck = interpolate.splrep(range(ranget),data,s=0)
		x = np.arange(0,23,0.1)
		y = interpolate.splev(x,tck,der=0)
		plt.plot(x,y,linestyle,label=label,linewidth=2)
	plt.xlim(0,ranget-1)
	plt.ylim(0,12)
	plt.xlabel('Time /hour')
	plt.ylabel('User ($\\times 10^{4}$)')
	handles, labels = ax.get_legend_handles_labels()
	ax.legend(handles,labels,loc=4)
	xmajorLocator = MultipleLocator(1)
	xmajorFormatter = FormatStrFormatter('%d')
	ax.xaxis.set_major_locator(xmajorLocator)
	ax.xaxis.set_major_formatter(xmajorFormatter)
	# show()
	for postfix in ('eps','png'):
		savefig('../figure/{0}/03.{0}'.format(postfix))


if __name__ == "__main__":
	statistic_hour_user()

