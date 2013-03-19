#!/usr/bin/env python
# Author: Yunqi Zhang
# Email: yqzhang@ucsd.edu

from Utils import Utils
from IPtoRouter import IPRouter
from FailureVerifier import PingFailureVerifier
from LinkMap import LinkMap
from ISISFailure import Failure
from ISISFailure import ISISFailure

class RoutingPerformance:
	# Source ID Map for ping data
	SourceIDMap = {'ucsb':0,'ucla':1,'ucsd':2,'ucdavis':3,'berkeley':4,'ucsc':5}
	util = Utils()
	#iprouter = IPRouter()
	verifier = PingFailureVerifier()
	linkMap = LinkMap()
	failureList = list()

	def __init__(self):
		self.util.ReadFormatedPingDataIntoMemory()
		self.failureList = self.failureList = ISISFailure().traverse()

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
			if hop != None and hop != "":
				return hop

	def getLastHop(self, path):
		return path[len(path) - 1].strip()

	def parsePerformance(self):
		perf = open("../plot/routing_performance.dat", "w")
		output_buffer = "Route\tActual_Path_Weight\tOptimal_Path_Weight\n"

		ite = 0
		count = 0
		equal = 0
		for ping in self.util.FindPing('', ''):
			ite += 1
			if ite % 1000 == 0:
				print("Loop:" + str(ite))
			# Get rid of \r
			path = self.verifier.getPath(ping)
			#print(ping)
			if self.ifDetectable(path):
				count += 1
				actualWeight = self.linkMap.calWeight(path)
				optimalWeight = self.linkMap.getRealtimeShortestPath(self.getFirstHop(path), self.getLastHop(path), ping[0], self.failureList)[1]
				if actualWeight == optimalWeight:
					equal += 1
				#print("Actual:" + str(actualWeight) + " Optimal:" + str(optimalWeight))
				output_buffer += str(count) + "\t" + str(actualWeight) + "\t" + str(optimalWeight) + "\n"
			else:
				continue
		print("Total detectable route count: " + str(count))
		print("Equal path weights count: " + str(equal))
		perf.write(output_buffer)
					

rp = RoutingPerformance()
rp.parsePerformance()
