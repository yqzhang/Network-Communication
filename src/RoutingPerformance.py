#!/usr/bin/env python
# Author: Yunqi Zhang
# Email: yqzhang@ucsd.edu

from Utils import Utils
from IPtoRouter import IPRouter
from FailureVerifier import PingFailureVerifier
from LinkMap import LinkMap

class RoutingPerformance:
	# Source ID Map for ping data
	SourceIDMap = {'ucsb':0,'ucla':1,'ucsd':2,'ucdavis':3,'berkeley':4,'ucsc':5}
	util = Utils()
	iprouter = IPRouter()
	verifier = PingFailureVerifier()
	linkMap = LinkMap()

	def __init__(self):
		self.util.ReadFormatedPingDataIntoMemory()

	def ifDetectable(self, path):
		for i in range(len(path)):
			if path[i] != None and path[i] != "":
				break
		if i == len(path) - 1:
			return False
		for j in range(i, len(path)):
			if path[j] == None or path[j].strip() == "":
				return False
		return True

	def getFirstHop(self, path):
		for hop in path:
			if hop != "":
				return hop

	def getLastHop(self, path):
		return path[len(path) - 1].strip()

	def parsePerformance(self):
		perf = open("../plot/routing_performance.dat", "w")
		output_buffer = ""

		count = 0
		for ping in self.util.FindPing('', ''):
			# Get rid of \r
			path = self.verifier.getPath(ping)
			print(path)
			if self.ifDetectable(path):
				count += 1
				actualWeight = self.linkMap.calWeight(path)
				optimalWeight = self.linkMap.getShortestPath(self.getFirstHop(path), self.getLastHop(path))
				print("Actual:" + str(actualWeight) + " Optimal:" + str(optimalWeight))
				output_buffer += str(count) + "\t" + str(actualWeight) + "\t" + str(optimalWeight) + "\n"
			else:
				continue
		print("Total detectable route count: " + str(count))
		perf.write(output_buffer)
					

rp = RoutingPerformance()
rp.parsePerformance()
