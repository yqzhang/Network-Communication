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

	def parsePerformance(self):
		for ping in self.util.FindPing('', ''):
			# Get rid of \r
			path = self.verifier.getPath(ping)
			actualWeight = self.linkMap.calWeight(path)
			print(actualWeight)
					

rp = RoutingPerformance()
rp.parsePerformance()
