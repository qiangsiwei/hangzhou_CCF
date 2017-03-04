# -*- coding: utf-8 -*- 

import glob
import fileinput
from pylab import *

# 时间粒度为1小时
# 空间粒度为200米
# 20-24为工作日

ranget, rangex, rangey = 24, 225, 150

def statistic_user_hour_distance():
	fig = plt.figure()

	wds, wes = ['0820','0821','0822','0823','0824'], ['0819','0825','0826']
	day, stat = [[[] for j in xrange(ranget)] for i in xrange(2)], [[[0,0] for j in xrange(ranget)] for i in xrange(2)]
	
	for d, (flist, label) in enumerate([(wds,"weekdays"),(wes,"weekends")]):
		for filename in sorted(glob.glob(r"../data/user_hour_dist_bs/*")):
			if filename.split("/")[-1] in ["{0}.txt".format(fname) for fname in flist]:
				for line in fileinput.input(filename):
					part = line.strip().split(" ")
					t, dist = int(part[1]), int(part[2])
					stat[d][t][0] += 1
					if dist > 0:
						day[d][t].append(dist)
						stat[d][t][1] += 1
				fileinput.close()

		ax = fig.add_subplot(2,1,d+1)
		plt.xlim(0,ranget-1)
		plt.ylim(0,6000)
		ax.set_xlabel('Time /hour')
		ax.set_ylabel('Distance /m')
		plt.title('{0}'.format(label))
		ax.boxplot(day[d],0,'')
		
	subplots_adjust(wspace=0.2,hspace=0.4)
	# show()
	for postfix in ('eps','png'):
		savefig('../figure/{0}/05.{0}'.format(postfix))


if __name__ == "__main__":
	statistic_user_hour_distance()

