# -*- coding: utf-8 -*- 

import glob
import fileinput
import numpy as np

# 时间粒度为1小时
# 空间粒度为200米
# 20-24为工作日

ranget, rangex, rangey = 24, 225, 150

def flow_prediction(method=""):
	record = [[[[0]*ranget for j in xrange(rangey)] for i in xrange(rangex)] for d in xrange(8)]
	for d, filename in enumerate(sorted(glob.glob(r"../data/pos_hour_user#/*"))):
		print filename
		for line in fileinput.input(filename):
			part = line.strip().split(" ")
			px, py, t, c = int(part[0].split(",")[0]), int(part[0].split(",")[1]), int(part[1]), int(part[2])
			record[d][px][py][t] = c
		fileinput.close()
	record = filter(lambda x:sum(x)>=10*ranget, [record[d][i][j] for d in xrange(8) for i in xrange(rangex) for j in xrange(rangey)])

	if method == "RNN":
		from keras.models import Graph
		from keras.layers import recurrent, Dropout, TimeDistributedDense
		normal = [[1.*record[r][t]/max(record[r]) for t in xrange(ranget)] for r in xrange(len(record))]
		X_train = np.array([[[p] for p in r][:-1] for r in normal])
		y_train = np.array([[[p] for p in r][1:] for r in normal])
		EPOCH_SIZE = 5
		HIDDEN_SIZE = 256
		RNN = recurrent.GRU # Replace with SimpleRNN, LSTM, GRU
		model = Graph()
		model.add_input(name='input', input_shape=(ranget-1,1))
		model.add_node(RNN(HIDDEN_SIZE, return_sequences=True), name='forward_l1', input='input')
		model.add_node(TimeDistributedDense(1), name='dense', input='forward_l1')
		model.add_output(name='output', input='dense')
		model.compile('adam', {'output': 'mean_squared_error'})
		model.fit({'input': X_train, 'output': y_train}, nb_epoch=EPOCH_SIZE, show_accuracy=True)
		y_pred = model.predict({'input': X_train})['output']
		y_error_total, y_real_total = np.zeros((23,)), np.zeros((23,))
		for r in xrange(len(record)):
			y_error_total += abs(np.reshape(max(record[r])*y_pred[r],(23,))-np.array(record[r][1:]))
			y_real_total += np.array(record[r][1:])
		print 1.*y_error_total/y_real_total

	if method == "ARIMA":
		from statsmodels.tsa.arima_model import ARIMA
		normal = np.array(normal)[np.random.choice(len(record), 100)]
		y_error_total, y_real_total = np.zeros((23,)), np.zeros((23,))
		for x in normal:
			try:
				model = ARIMA(np.array(x), order=(2,0,1)).fit(disp=False)
				y_error_total += abs(model.predict(1,23)-np.array(x[1:]))
				y_real_total += np.array(x[1:])
			except:
				continue
		print 1.*y_error_total/y_real_total

def plot_error():
	from pylab import *
	from scipy import interpolate
	from matplotlib.ticker import MultipleLocator, FormatStrFormatter

	error_RNN = [0]*6 +\
				[0.27470582,0.26526711,0.17191297,0.17505597,0.16296111,0.14432448,\
				0.13287850,0.13018013,0.12400923,0.12198262,0.12254024,0.13259150,\
				0.15847546,0.15153314,0.15145022,0.13929038,0.14714874,0.17220128]
	error_ARIMA = [0]*6 +\
				[0.39960266,0.43644585,0.21430307,0.26086768,0.18084257,0.24340537,\
				0.18037208,0.19926624,0.17947106,0.17663812,0.21210755,0.27719361,\
				0.17571100,0.19287534,0.17002414,0.19231532,0.21721267,0.29783381]
	fig = plt.figure()
	ax1 = fig.add_subplot(111)
	for error, linestyle, label in [(error_RNN,'k-',"RNN"), (error_ARIMA,'k--',"ARIMA")]:
		tck = interpolate.splrep(range(len(error)),error,s=0)
		xnew = np.arange(0,ranget,0.1)
		ynew = interpolate.splev(xnew,tck,der=0)
		plt.plot(xnew,ynew,linestyle,label=label,linewidth=2)
	plt.xlim(6,23)
	plt.ylim(0,0.6)
	plt.xlabel('The $N$-th hour of day')
	plt.ylabel('Error')
	handles, labels = ax1.get_legend_handles_labels()
	ax1.legend(handles, labels)
	xmajorLocator = MultipleLocator(1)
	xmajorFormatter = FormatStrFormatter('%d')
	ax1.xaxis.set_major_locator(xmajorLocator)
	ax1.xaxis.set_major_formatter(xmajorFormatter)
	# show()
	for postfix in ('eps','png'):
		plt.savefig('../figure/{0}/16.{0}'.format(postfix))


if __name__ == "__main__":
	# flow_prediction(method="RNN")
	# flow_prediction(method="ARIMA")
	plot_error()

