# -*- coding: utf-8 -*- 

import sys
from operator import add
from pyspark import SparkConf
from pyspark import SparkContext

# basics
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
				gx, gy = int((lng-120.02)/(120.48-120.02)*225), int((lat-30.15)/(30.42-30.15)*150)
				return (str(gx)+","+str(gy), sl, IMSI)
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
	# user#
	lines = sc.textFile("hdfs://namenode.omnilab.sjtu.edu.cn/user/qiangsiwei/hangzhou/original/{0}.csv".format(filename))
	counts = lines.map(lambda x : extract(x))\
			.filter(lambda x : x[0]!="" and x[1]!=-1 and x[2]!="")\
			.map(lambda x : (x[2]))\
			.distinct() \
			.map(lambda x : ("user#",1)) \
			.reduceByKey(add) \
			.map(lambda x : str(x[0])+" "+str(x[1]))
	output = counts.coalesce(1).saveAsTextFile("./hangzhou/CFF/{0}_basics_user#.csv".format(filename))
	# entry#
	lines = sc.textFile("hdfs://namenode.omnilab.sjtu.edu.cn/user/qiangsiwei/hangzhou/original/{0}.csv".format(filename))
	counts = lines.map(lambda x : ("entry#",1)) \
			.reduceByKey(add) \
			.map(lambda x : str(x[0])+" "+str(x[1]))
	output = counts.coalesce(1).saveAsTextFile("./hangzhou/CFF/{0}_basics_entry#.csv".format(filename))
