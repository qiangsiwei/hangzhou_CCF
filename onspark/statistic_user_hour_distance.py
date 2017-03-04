# -*- coding: utf-8 -*- 

import sys
from operator import add
from pyspark import SparkConf
from pyspark import SparkContext

# user_hour_distance2
def rd(x):
	import math
	dist_max = 0
	if len(x) >= 2:
		for i in range(0,len(x)-1):
			for j in range(i+1,len(x)):
				p1, p2 = [float(k) for k in x[i].split(",")], [float(k) for k in x[j].split(",")]
				lng1,lat1,lng2,lat2 = p1[0],p1[1],p2[0],p2[1]
				earth_radius, radlat1, radlat2 = 6400*1000, lat1*math.pi/180.0, lat2*math.pi/180.0
				a, b = radlat1-radlat2, lng1*math.pi/180.0-lng2*math.pi/180.0
				s = 2*math.asin(math.sqrt(math.pow(math.sin(a/2),2)+math.cos(radlat1)*math.cos(radlat2)*math.pow(math.sin(b/2),2)))
				dist = int(abs(s*earth_radius))
				dist_max = dist if dist > dist_max else dist_max
	return dist_max

def extract(line):
	import time
	try:
		part = line.strip().replace('\"','').split(",")
		TTIME, LAC, CI, IMSI = part[1].split(" "), part[3], part[4], part[5]
		pt1, pt2, pt3 = TTIME[0].split("-"), TTIME[1].split("."), TTIME[2]
		year, month, day, hour, minute, second = int("20"+pt1[2]), {"AUG":8}[pt1[1]], int(pt1[0]), int(pt2[0]), int(pt2[1]), int(pt2[2])
		hour = hour if hour != 12 else 0
		hour = hour if pt3 == "AM" else hour+12
		secs = hour*3600+minute*60+second
		key = LAC+" "+CI
		sl = secs/3600
		if bss.has_key(key):
			bs = bss[key]
			lng, lat = bs["lng"], bs["lat"]
			if 120.02<=lng<120.48 and 30.15<=lat<=30.42:
				return (str(lng)+","+str(lat), sl, IMSI)
			else:
				return ("", -1, "")
		else:
			return ("", -1, "")
	except:
		return ("", -1, "")

global bss

if __name__ == "__main__":
	import fileinput
	bss = {}
	for line in fileinput.input("hz_base.txt"):
		part = line.strip().split(" ")
		num, lng, lat = part[1]+" "+part[2], float(part[3]), float(part[4])
		bss[num] = {"lng":lng, "lat":lat}
	fileinput.close()
	conf = SparkConf().setMaster('yarn-client') \
				  .setAppName('qiangsiwei') \
				  .set('spark.driver.maxResultSize', "8g")
	sc = SparkContext(conf = conf)
	filename = "0819"
	lines = sc.textFile("hdfs://namenode.omnilab.sjtu.edu.cn/user/qiangsiwei/hangzhou/original/{0}.csv".format(filename))
	counts = lines.map(lambda x : extract(x)) \
			.filter(lambda x : x[0]!="" and x[1]!=-1 and x[2]!="") \
			.map(lambda x : ((x[2],x[1]),x[0]))\
			.distinct() \
			.groupByKey() \
			.map(lambda x : (x[0],rd(list(x[1])))) \
			.map(lambda x : str(x[0][0])+" "+str(x[0][1])+" "+str(x[1]))
	output = counts.saveAsTextFile("./hangzhou/CFF/{0}_user_hour_dist_bs.csv".format(filename))
