#!/usr/bin/env python
# Author: Yunqi Zhang
# Email: yqzhang@ucsd.edu

from ISISFailure import Failure
from ISISFailure import ISISFailure
from Utils import Utils
from IPtoRouter import IPRouter

# Description:
# Go through all the IS-IS failures (obtained from ISISFailure.py)
# For each failure, try to find the failure in the traceroute data
# files (obtained from ProcessPingData.py)

class FailureDetection:
	failureList = list()
	util = Utils()
	iprouter = IPRouter()

	# Source ID Map for ping data
	SourceIDMap = {'ucsb':0,'ucla':1,'ucsd':2,'ucdavis':3,'berkeley':4,'ucsc':5}

	def __init__(self):
		# Initiate the failure list from ISISFailure.py
		# Format: router1, port1, router2, port2, failure_start, failure_end
		self.failureList = ISISFailure().traverse()
		# Initiate Utils
		self.util.ReadFormatedPingDataIntoMemory()

	def lookUpByIP(self, IP, failure_start, failure_end):
		# Look up the ping data from Utils.py
		# Search by IP address
		retval = dict()
		retval["BEFORE"] = dict()
		retval["DURING"] = dict()
		retval["AFTER"]  = dict()
		failure_start = float(failure_start)
		failure_end = float(failure_end)
		
		for i in range(6):
			ifBefore = True
			preData = None
			retval["BEFORE"][i] = None
			retval["DURING"][i] = None
			retval["AFTER"][i]  = None
			for data in self.util.FindPing(i, IP):
				if data[1] < failure_start:
					# Before
					preData = data
				elif data[0] > failure_start and ifBefore == True:
					# During
					retval["BEFORE"][i] = preData
					retval["DURING"][i] = data
					ifBefore = False
				elif data[0] > failure_end:
					# After
					retval["AFTER"][i] = data
					break

		return retval

	def lookUpByRouter(self, router, port, failure_start, failure_end):
		#Convert router:port to IP and call lookUpByIP()
		ip_start = self.iprouter.query_by_router(router, port, failure_start)
		ip_end = self.iprouter.query_by_router(router, port, failure_end)
		if ip_start != ip_end:
			# TODO: We need to figure it out if this happens a lot
			print("Error! IP address changed during failure.")
			return None
		else:
			return self.lookUpByIP(ip_start, failure_start, failure_end)

	def lookUp(self):
		# Traverse the failure list and look them up
		for fail in self.failureList:
			router1 = fail[0]
			port1 = fail[1]
			router2 = fail[2]
			port2 = fail[3]
			failure_start = fail[4]
			failure_end = fail[5]
			# Format: router1, port1, router2, port2, failure_start, failure_end
			src_ping = self.lookUpByRouter(router1, port1, failure_start, failure_end)
			dst_ping = self.lookUpByRouter(router2, port2, failure_start, failure_end)
			for i in range(6):
				if src_ping["BEFORE"][i] != None:
					# Before failure
					print("Before failure:")
					print(src_ping["BEFORE"][i])
					# During failure
					print("During failure:")
					print(src_ping["DURING"][i])
					# After failure
					print("After failure:")
					print(src_ping["AFTER"][i])
				if src_ping["BEFORE"][i] != None:
					# Before failure
					print("Before failure:")
					print(dst_ping["BEFORE"][i])
					# During failure
					print("During failure:")
					print(dst_ping["DURING"][i])
					# After failure
					print("After failure:")
					print(dst_ping["AFTER"][i])

fd = FailureDetection()
fd.lookUp()
