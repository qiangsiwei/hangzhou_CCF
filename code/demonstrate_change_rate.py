# -*- coding: utf-8 -*- 

import glob
import fileinput
import numpy as np
from pylab import *

# 时间粒度为1小时
# 空间粒度为200米
# 20-24为工作日

ranget, rangex, rangey = 24*2, 225, 150

def generate_equilibrium():
	equilibrium = [[[[[0,0,0,0] for k in xrange(ranget-1)] for j in xrange(rangey)] for i in xrange(rangex)] for d in xrange(8)]
	for d, filename in enumerate(sorted(glob.glob(r"../data/pos_30min_usergroup/*"))):
		print filename
		mesh = [[[[] for k in xrange(ranget)] for j in xrange(rangey)] for i in xrange(rangex)]
		for line in fileinput.input(filename):
			part = line.strip().split(" ")
			px, py, t, n = int(part[0].split(",")[0]), int(part[0].split(",")[1]), int(part[1]), part[2:]
			mesh[px][py][t] = n
		fileinput.close()
		for i in xrange(rangex):
			for j in xrange(rangey):
				for t in xrange(ranget-1):
					leave = len(set(mesh[i][j][t]).difference(set(mesh[i][j][t+1])))
					enter = len(set(mesh[i][j][t+1]).difference(set(mesh[i][j][t])))
					stay = len(set(mesh[i][j][t+1]).intersection(set(mesh[i][j][t])))
					equilibrium[d][i][j][t] = [leave, enter, enter-leave, stay]

	with open("../data/var/equilibrium.txt","w") as f:
		for i in xrange(rangex):
			for j in xrange(rangey):
				f.write("{0},{1}\t{2}\n".format(i,j,"\t".join([" ".join([",".join([str(x) for x in equilibrium[d][i][j][t]])\
																for t in xrange(ranget-1)]) for d in xrange(8)])))

def demonstrate_change_rate():
	tseq = [8,12,16,20]
	stat = [[0 for j in xrange(rangey)] for i in xrange(rangex)]
	for filename in sorted(glob.glob(r"../data/pos_hour_user#/*"))[1:8]:
		for line in fileinput.input(filename):
			part = line.strip().split(" ")
			px, py, t, n = int(part[0].split(",")[0]), int(part[0].split(",")[1]), int(part[1]), int(part[2])
			stat[px][py] += n
		fileinput.close()
	stat = [[stat[i][j]/7 for j in xrange(rangey)] for i in xrange(rangex)]

	mesh = [[[0 for j in xrange(rangey)] for i in xrange(rangex)] for t in xrange(len(tseq))]
	equilibrium = [[[] for j in xrange(rangey)] for i in xrange(rangex)]
	for line in fileinput.input("../data/var/equilibrium.txt"):
		part = line.strip().split("\t")
		px, py, d = int(part[0].split(",")[0]), int(part[0].split(",")[1]), [[[int(k) for k in j.split(",")] for j in i.split(" ")] for i in part[1:]]
		equilibrium[px][py] = d
		if stat[px][py] >= 500:
			leave = [sum([equilibrium[px][py][d][t][0] for d in xrange(1,8)])/7 for t in xrange(ranget-1)]
			enter = [sum([equilibrium[px][py][d][t][1] for d in xrange(1,8)])/7 for t in xrange(ranget-1)]
			stay = [sum([equilibrium[px][py][d][t][3] for d in xrange(1,8)])/7 for t in xrange(ranget-1)]
			for p, t in enumerate(tseq):
				mesh[p][px][py] = sum([float((leave[i]+enter[i])/2)/(stay[i]+1) for i in xrange(len(stay))][2*t-1:2*t+3])/4
	fileinput.close()

	plt.figure(figsize=(10,8))
	levels, norm = arange(0, 20, 1), cm.colors.Normalize(vmax=20, vmin=0)
	for c, t in enumerate(tseq):
		(X, Y), C = meshgrid(np.arange(100), np.arange(100)), np.array(mesh[c])[20:120,20:120]
		subplot(2,2,c+1)
		cset1 = pcolormesh(X, Y, C.T, cmap=cm.get_cmap("Reds", len(levels)), norm=norm)
		plt.axis([0, 100-1, 0, 100-1])
		plt.xticks(np.linspace(0,100,6))
		plt.yticks(np.linspace(0,100,6))
		plt.title('{0}:00 - {1}:00'.format(str(t).zfill(2),str(t+2).zfill(2)))
		if c == 0:
			plt.xlabel('Longitude grid index /200m')
			plt.ylabel('Latitude grid index /200m')
		if c == 2:
			subplots_adjust(hspace=0.4)
	subplots_adjust(bottom=0.1, left=0.1, right=0.9, top=0.9)
	cax2 = axes([0.92, 0.10, 0.01, 0.8])
	colorbar(cax=cax2)
	show()
	# for postfix in ('eps','png'):
	# 	savefig('../figure/{0}/09.{0}'.format(postfix))

def demonstrate_change_ratio(generate_log=True):
	from scipy import interpolate
	from matplotlib.ticker import MultipleLocator, FormatStrFormatter

	if generate_log:
		wds, wes = range(1,6), range(0,1)+range(6,8)
		equilibrium = [[[] for j in xrange(rangey)] for i in xrange(rangex)]
		leave_wd_stat, enter_wd_stat, stay_wd_stat = [0 for i in xrange(ranget-1)], [0 for i in xrange(ranget-1)], [0 for i in xrange(ranget-1)]
		leave_we_stat, enter_we_stat, stay_we_stat = [0 for i in xrange(ranget-1)], [0 for i in xrange(ranget-1)], [0 for i in xrange(ranget-1)]

		for line in fileinput.input("../data/var/equilibrium.txt"):
			part = line.strip().split("\t")
			px, py, day = int(part[0].split(",")[0]), int(part[0].split(",")[1]), [[[int(k) for k in j.split(",")] for j in i.split(" ")] for i in part[1:]]
			equilibrium[px][py] = day
			leave_wd = [sum([equilibrium[px][py][d][t][0] for d in wds])/len(wds) for t in xrange(ranget-1)]
			enter_wd = [sum([equilibrium[px][py][d][t][1] for d in wds])/len(wds) for t in xrange(ranget-1)]
			stay_wd = [sum([equilibrium[px][py][d][t][3] for d in wds])/len(wds) for t in xrange(ranget-1)]
			leave_we = [sum([equilibrium[px][py][d][t][0] for d in wes])/len(wds) for t in xrange(ranget-1)]
			enter_we = [sum([equilibrium[px][py][d][t][1] for d in wes])/len(wes) for t in xrange(ranget-1)]
			stay_we = [sum([equilibrium[px][py][d][t][3] for d in wes])/len(wes) for t in xrange(ranget-1)]
			leave_wd_stat, enter_wd_stat, stay_wd_stat = [i+j for i,j in zip(leave_wd_stat,leave_wd)], [i+j for i,j in zip(enter_wd_stat,enter_wd)], [i+j for i,j in zip(stay_wd_stat,stay_wd)]
			leave_we_stat, enter_we_stat, stay_we_stat = [i+j for i,j in zip(leave_we_stat,leave_we)], [i+j for i,j in zip(enter_we_stat,enter_we)], [i+j for i,j in zip(stay_we_stat,stay_we)]
		fileinput.close()

		with open("../data/var/mobility.txt","w") as f:
			f.write(" ".join([str(float((leave_wd_stat[i]+enter_wd_stat[i])/2)/(stay_wd_stat[i])) for i in xrange(len(stay_wd_stat))])+"\n")
			f.write(" ".join([str(float((leave_we_stat[i]+enter_we_stat[i])/2)/(stay_we_stat[i])) for i in xrange(len(stay_we_stat))])+"\n")

	ratio1 = [float(i) for i in open("../data/var/mobility.txt","r").read().split('\n')[0].split(" ")]
	ratio2 = [float(i) for i in open("../data/var/mobility.txt","r").read().split('\n')[1].split(" ")]
	maximum, minimum = max(max(ratio1),max(ratio2)), min(min(ratio1),min(ratio2))
	ratio1 = [(i-minimum)/(maximum-minimum) for i in ratio1]
	ratio2 = [(i-minimum)/(maximum-minimum) for i in ratio2]

	fig = plt.figure()
	ax = fig.add_subplot(111)
	for y, linestyle, label in [(ratio1,'k-',"Weekday"), (ratio2,'k--',"Weekend")]:
		tck = interpolate.splrep([i/2.0 for i in xrange(ranget-1)] ,y,s=0)
		x = np.arange(0,23,0.1)
		y = interpolate.splev(x,tck,der=0)
		plt.plot(x,y,linestyle,label=label,linewidth=2)
	plt.xlim(0,23)
	plt.ylim(0,1.05)
	plt.xlabel('Time /hour')
	plt.ylabel('Mobility Rate')
	handles, labels = ax.get_legend_handles_labels()
	ax.legend(handles,labels)
	xmajorLocator = MultipleLocator(1)
	xmajorFormatter = FormatStrFormatter('%d')
	ax.xaxis.set_major_locator(xmajorLocator)
	ax.xaxis.set_major_formatter(xmajorFormatter)
	# show()
	for postfix in ('eps','png'):
		savefig('../figure/{0}/10.{0}'.format(postfix))


if __name__ == "__main__":
	# generate_equilibrium()
	demonstrate_change_rate()
	# demonstrate_change_ratio(generate_log=False)

