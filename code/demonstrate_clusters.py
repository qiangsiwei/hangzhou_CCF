# -*- coding: utf-8 -*- 

import fileinput
import numpy as np
from pylab import *
from constant import *

# 时间粒度为1小时
# 空间粒度为200米
# 20-24为工作日

ranget, rangex, rangey = 24, 225, 150

def demonstrate_examples():
	from scipy import interpolate
	from matplotlib.ticker import MultipleLocator, FormatStrFormatter

	differentiate = {}
	for line in fileinput.input("../data/var/weekday.txt"):
		part = line.strip().split(" ")
		x, y, f = int(part[0]), int(part[1]), [float(i) for i in part[2:]]
		differentiate[(x,y)] = f
	fileinput.close()

	fig = plt.figure()
	ax1 = fig.add_subplot(111)
	for lng, lat, linestyle, label in [(120.206,30.282,'k-',"A"), (120.132,30.280,'k--',"B"), (120.176,30.310,'k:',"C")]:
		px, py = int((lng-lng_min)/(lng_max-lng_min)*rangex), int((lat-lat_min)/(lat_max-lat_min)*rangey)
		x, y = [i for i in xrange(ranget)], differentiate[tuple((px,py))]
		tck = interpolate.splrep(x,y,s=0)
		xnew = np.arange(0,23,0.1)
		ynew = interpolate.splev(xnew,tck,der=0)
		plt.plot(xnew,ynew,linestyle,label=label,linewidth=2)
	plt.plot([0,23],[0,0],'k--')
	plt.xlim(0,23)
	plt.ylim(-0.06,0.06)
	plt.xlabel('Time /hour')
	plt.ylabel('Difference index')
	handles, labels = ax1.get_legend_handles_labels()
	ax1.legend(handles, labels)
	xmajorLocator = MultipleLocator(1)
	xmajorFormatter = FormatStrFormatter('%d')
	ax1.xaxis.set_major_locator(xmajorLocator)
	ax1.xaxis.set_major_formatter(xmajorFormatter)
	# show()
	for postfix in ('eps','png'):
		savefig('../figure/{0}/12.{0}'.format(postfix))

def demonstrate_clusters():
	from sklearn.cluster import KMeans
	from scipy import interpolate
	from matplotlib.ticker import MultipleLocator, FormatStrFormatter

	plist, X = [], []
	for line in fileinput.input("../data/var/weekday.txt"):
		part = line.strip().split(" ")
		x, y, f = int(part[0]), int(part[1]), [float(i) for i in part[2:]]
		plist.append([x,y])
		X.append(f)
	fileinput.close()

	k_means = KMeans(init='k-means++', n_clusters=3, n_init=10)
	k_means.fit(X)
	k_means.labels_ = k_means.labels_
	k_means.cluster_centers_ = k_means.cluster_centers_

	mesh = [[0 for j in xrange(rangey)] for i in xrange(rangex)]
	for i in xrange(len(k_means.labels_)):
		if k_means.labels_[i] == 0:
			mesh[plist[i][0]][plist[i][1]] = 1.5
		if k_means.labels_[i] == 1:
			mesh[plist[i][0]][plist[i][1]] = 0.6
		if k_means.labels_[i] == 2:
			mesh[plist[i][0]][plist[i][1]] = -1

	fig = plt.figure()
	ax = fig.add_subplot(111)
	(X, Y), C = meshgrid(np.arange(100), np.arange(100)), np.array(mesh)[20:120,20:120]
	pcolormesh(X, Y, C.T, cmap='RdBu', vmin=-2, vmax=2)
	plt.axis([0, 100-1, 0, 100-1])
	plt.xlabel('Longitude grid index /200m')
	plt.ylabel('Latitude grid index /200m')
	# plt.show()
	for postfix in ('eps','png'):
		savefig('../figure/{0}/13.{0}'.format(postfix))

	fig = plt.figure()
	ax1 = fig.add_subplot(111)
	for _cluster, linestyle, label in [(0,'k-',"Cluster 1"), (1,'k--',"Cluster 2"), (2,'k:',"Cluster 3")]:
		x, y = [i for i in xrange(ranget)], k_means.cluster_centers_[_cluster]
		tck = interpolate.splrep(x,y,s=0)
		xnew = np.arange(0,23,0.1)
		ynew = interpolate.splev(xnew,tck,der=0)
		plt.plot(xnew,ynew,linestyle,label=label,linewidth=2)
	plt.plot([0,23],[0,0],'k--')
	plt.xlim(0,23)
	plt.ylim(-0.03,0.03)
	plt.xlabel('Time /hour')
	plt.ylabel('Differentiate index')
	handles, labels = ax1.get_legend_handles_labels()
	ax1.legend(handles, labels)
	xmajorLocator = MultipleLocator(1)
	xmajorFormatter = FormatStrFormatter('%d')
	ax1.xaxis.set_major_locator(xmajorLocator)
	ax1.xaxis.set_major_formatter(xmajorFormatter)
	# show()
	for postfix in ('eps','png'):
		savefig('../figure/{0}/14.{0}'.format(postfix))


if __name__ == "__main__":
	# demonstrate_examples()
	demonstrate_clusters()

