#!/usr/bin/env python
# Author: Yunqi Zhang
# Email: yqzhang@ucsd.edu

from ISISFailure import Failure
from ISISFailure import ISISFailure
from Utils import Utils
from IPtoRouter import IPRouter
from datetime import datetime

class FailureStatistics:
	failureList = list()
	failureMap = dict()

	def __init__(self):
		# Initiate the failure list from ISISFailure.py
		# Format: router1, port1, router2, port2, failure_start, failure_end
		self.failureList = ISISFailure().traverse()

	def failurePlot(self):
		for fail in self.failureList:
			router1 = fail[0]
			port1 = fail[1]
			router2 = fail[2]
			port2 = fail[3]
			failure_start = float(fail[4])
			failure_end = float(fail[5])
			fail_key = router1 + ":" + port1 + "," + router2 + ":" + port2

			if fail_key not in self.failureMap:
				self.failureMap[fail_key] = list()

			temp = dict()
			temp["start"] = datetime.fromtimestamp(int(failure_start)).strftime("%m-%d-%Y %H:%M:%S")
			temp["end"] = datetime.fromtimestamp(int(failure_end)).strftime("%m-%d-%Y %H:%M:%S")
			self.failureMap[fail_key].append(temp)

		plot = open("../plot/failure_plot.dat", "w")
		dis = open("../plot/failure_distribution.dat", "w")
		prob = [0] * 9512
		output_buffer = ""

		count = 0
		for key, value in self.failureMap.items():
			count += 1
			prob[len(value)] += 1
			for fail in value:
				output_buffer += str(count) + "\t" + str(fail["start"]) + "\n"
				output_buffer += str(count) + "\t" + str(fail["end"]) + "\n"
				output_buffer += "\n"
		plot.write(output_buffer)

		accum = 0
		output_buffer = ""
		for i in range(9512):
			accum += prob[i]
			output_buffer += str(i) + "\t" + str(float(accum) / float(count)) + "\n"
		dis.write(output_buffer)

fs = FailureStatistics()
fs.failurePlot()
