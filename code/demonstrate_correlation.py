# -*- coding: utf-8 -*- 

import math
import fileinput

# 时间粒度为1小时
# 空间粒度为200米
# 20-24为工作日

ranget, rangex, rangey = 24, 225, 150

def euclidean(p1,p2):
	dist = math.sqrt(sum([pow(i-j,2) for i,j in zip(p1,p2)]))
	return dist

def demonstrate_correlation(function=""):
	if function == "generate_log":
		plist = []
		for line in fileinput.input("../data/var/weekday.txt"):
			part = line.strip().split(" ")
			x, y, f = int(part[0]), int(part[1]), [float(i) for i in part[2:]]
			plist.append([[x,y],f])
		fileinput.close()

		covariance = {}
		for i in range(0, len(plist)-1):
			for j in range(i+1, len(plist)):
				dist = int(round(euclidean(plist[i][0], plist[j][0]),0))
				covariance[dist] = covariance.get(dist,[0,0,0])
				covariance[dist][0] += 1 
				covariance[dist][1] += sum([plist[i][1][t]*plist[j][1][t] for t in xrange(24)])
				covariance[dist][2] += sum([(plist[i][1][t]**2+plist[j][1][t]**2)/2 for t in xrange(24)])
		covariance = sorted([{'d':d,'v':covariance[d]} for d in covariance], key=lambda x:x['d'], reverse=False)
		
		with open("../data/var/covariance.txt","w") as f:
			for e in covariance:
				f.write("{0}\t{1}\t{2}\n".format(e['d']*200,e['v'][0],e['v'][1]/e['v'][2]))

	if function == "plot_correlation":
		import numpy as np
		from pylab import *

		covariance = {}
		for line in fileinput.input("../data/var/covariance.txt"):
			d, r = int(line.strip().split('\t')[0]), float(line.strip().split('\t')[2])
			covariance[d] = r

		fig = plt.figure()
		ax = fig.add_subplot(111)
		ax.semilogx([(d+1)*200 for d in range(50)], [covariance[(d+1)*200] for d in range(50)],'k-',linewidth=2,label="correlation")
		ax.plot([100,2750],[0.5,0],'k:',linewidth=2,label="fitting")
		ax.plot([100,20000],[0,0],'k--')
		plt.xlim(100,20000)
		plt.ylim(-0.1,0.5)
		plt.xlabel('Distance /m')
		plt.ylabel('Correlation')
		handles, labels = ax.get_legend_handles_labels()
		ax.legend(handles, labels)
		# plt.show()
		for postfix in ('eps','png'):
			savefig('../figure/{0}/15.{0}'.format(postfix))


if __name__ == "__main__":
	demonstrate_correlation(function="generate_log")
	demonstrate_correlation(function="plot_correlation")

