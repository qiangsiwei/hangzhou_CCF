# -*- coding: utf-8 -*- 

import glob
import fileinput
import numpy as np
from pylab import *
from constant import *

# 时间粒度为1小时
# 空间粒度为200米
# 20-24为工作日

ranget, rangex, rangey = 24, 225, 150

def demonstrate_hotspots(function=""):
	day = [[[[0]*ranget for j in xrange(rangey)]for i in xrange(rangex)] for d in xrange(8)]
	for d, filename in enumerate(sorted(glob.glob(r"../data/pos_hour_user#/*"))):
		print filename
		for line in fileinput.input(filename):
			part = line.strip().split(" ")
			px, py, s, c = int(part[0].split(",")[0]), int(part[0].split(",")[1]), int(part[1]), int(part[2])
			day[d][px][py][s] = c
		fileinput.close()

	if function == "plot_pattern":
		from sklearn.cluster import KMeans
		from matplotlib.ticker import MultipleLocator, FormatStrFormatter

		top = [[[0 for t in xrange(7*ranget)] for j in xrange(rangey)] for i in xrange(rangex)]
		seq = [[[day[d][i][j][s] for d in xrange(1,8) for s in xrange(ranget)] for j in xrange(rangey)] for i in xrange(rangex)]
		for t in xrange(7*ranget):
			itemlist = [{"p":[i,j],"v":seq[i][j][t]} for i in xrange(rangex) for j in xrange(rangey)]
			for item in sorted(itemlist, key=lambda x:x["v"], reverse=True)[0:30]:
				top[item["p"][0]][item["p"][1]][t] = 1
		disp = [{"v":top[i][j],"k":-1} for i in xrange(rangex) for j in xrange(rangey) if sum(top[i][j])!=0]

		k_means = KMeans(init='k-means++', n_clusters=3, n_init=10)
		k_means.fit([p["v"] for p in disp])
		k_means_labels = k_means.labels_
		k_means_cluster_centers = k_means.cluster_centers_
		for i in xrange(len(k_means_labels)):
			disp[i]["k"] = k_means_labels[i]
		disp = sorted(disp, key=lambda x:x["k"])
		
		fig = plt.figure(figsize=(6,5))
		ax = fig.add_subplot(111)
		(X, Y) = meshgrid(np.arange(7*ranget), np.arange(len(disp)))
		C = np.array([[x*1.5 for x in i["v"]] if i["k"]==0 else \
					  [x*0.6 for x in i["v"]] if i["k"]==1 else \
					  [x*-1 for x in i["v"]] for i in disp])
		# plt.pcolormesh(X, Y, C)
		plt.pcolormesh(X, Y, C, cmap='RdBu', vmin=-2, vmax=2)
		plt.xlim(0,7*ranget-1)
		plt.ylim(0,len(disp)-1)
		xmajorLocator = MultipleLocator(12)
		xmajorFormatter = FormatStrFormatter('%d')
		ax.xaxis.set_major_locator(xmajorLocator)
		ax.xaxis.set_major_formatter(xmajorFormatter)
		plt.xlabel('Time /hour')
		plt.ylabel('Region')
		for postfix in ('eps','png'):
			savefig('../figure/{0}/07.{0}'.format(postfix))

	if function == "generate_log":
		wds, wes, hotspots = [1,2,3,4,5], [0,6,7], {}
		for dlist, lable in [(wds,"wd"),(wes,"we")]:
			seq = [[[day[d][i][j][s] for d in dlist for s in xrange(ranget)] for j in xrange(rangey)] for i in xrange(rangex)]
			top = [[[0 for t in xrange(len(dlist)*ranget)] for j in xrange(rangey)] for i in xrange(rangex)]
			
			for t in xrange(len(dlist)*ranget):
				itemlist = [{"p":[i,j],"v":seq[i][j][t]} for i in xrange(rangex) for j in xrange(rangey)]
				for item in sorted(itemlist, key=lambda x:x["v"], reverse=True)[0:30]:
					top[item["p"][0]][item["p"][1]][t] = 1
			
			with open("../data/var/hotspot_{0}.txt".format(lable),"w") as f:
				for i in xrange(rangex):
					for j in xrange(rangey):
						if sum(top[i][j]) != 0:
							f.write("{0} {1} {2}\n".format(i,j," ".join([str(x) for x in top[i][j]])))
			
			for line in fileinput.input("../data/var/hotspot_{0}.txt".format(lable)):
				part = line.strip().split(" ")
				px, py, v = int(part[0]), int(part[1]), [int(i) for i in part[2:]]
				c1 = round(1.*sum([v[d*24+t] for t in range(8,20) for d in xrange(len(dlist))])/len(dlist),2)
				c2 = round(1.*sum([v[d*24+t] for t in range(0,8)+range(20,24) for d in xrange(len(dlist))])/len(dlist),2)
				hotspot = hotspots.get((px,py),[0,0,0,0])
				if lable == "wd":
					hotspot[:2] = [c1,c2]
				if lable == "we":
					hotspot[2:] = [c1,c2]
				hotspots[(px,py)] = hotspot
			fileinput.close()
		
		with open("../data/var/hotspots.txt","w") as f:
			for k,v in hotspots.iteritems():
				lng, lat = round(1.*k[0]/rangex*(lng_max-lng_min)+lng_min,3), round(1.*k[1]/rangey*(lat_max-lat_min)+lat_min,3)
				f.write("{0} {1} {2}\n".format(lng,lat," ".join([str(x) for x in v])))


if __name__ == "__main__":
	demonstrate_hotspots(function="plot_pattern")
	# demonstrate_hotspots(function="generate_log")

