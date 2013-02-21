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
	ipcounter = 0

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
		
		for i in range(6):
			ifBefore = True
			preData = None
			retval["BEFORE"][i] = None
			retval["DURING"][i] = None
			retval["AFTER"][i]  = None
			
			# Search by the last hop
			for data in self.util.FindPing(i, IP, 1):
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
		#if ip_start == None:
		#	print("%s,%s,%f,%f"%(router,port,failure_start,failure_end))
			
		ip_end = self.iprouter.query_by_router(router, port, failure_end)
		
		if ip_start == None or ip_end == None:
			#print("No IP addresses assigned T_T")
			self.ipcounter += 1		
		if ip_start != ip_end:
			# TODO: We need to figure it out if this happens a lot
			print("Error! IP address changed during failure.")
			return None
		else:
			#print(ip_start)
			#print(failure_start)
			#print(failure_end)
			return self.lookUpByIP(ip_start, failure_start, failure_end)

	def lookUp(self):
		# Output file "route_change.txt"
		file = open("route_change.txt", "w")
	
		# Traverse the failure list and look them up
		for fail in self.failureList:
			router1 = fail[0]
			port1 = fail[1]
			router2 = fail[2]
			port2 = fail[3]
			failure_start = float(fail[4])
			failure_end = float(fail[5])
			# Format: router1, port1, router2, port2, failure_start, failure_end
			src_ping = self.lookUpByRouter(router1, port1, failure_start, failure_end)
			dst_ping = self.lookUpByRouter(router2, port2, failure_start, failure_end)
			
			if src_ping == None and dst_ping == None:
				continue
			
			ifRouted = False
			for i in range(6):
				if src_ping == None:
					pass
				elif src_ping["BEFORE"][i] != None:
					ifRouted = True
					file.write("Trace Router from node %d to source:\n"%i)
					# Before failure
					file.write("\tBefore failure:\n")
					file.write("\t\t" + str(src_ping["BEFORE"][i]) + "\n")
					# During failure
					file.write("\tDuring failure:\n")
					file.write("\t\t" + str(src_ping["DURING"][i]) + "\n")
					# After failure
					file.write("\tAfter failure:\n")
					file.write("\t\t" + str(src_ping["AFTER"][i]) + "\n")
					
				if dst_ping == None:
					pass
				elif dst_ping["BEFORE"][i] != None:
					ifRouted = True
					file.write("Trace Router from node %d to destination:"%i)
					# Before failure
					file.write("\tBefore failure:\n")
					file.write("\t\t" + str(dst_ping["BEFORE"][i]) + "\n")
					# During failure
					file.write("\tDuring failure:\n")
					file.write("\t\t" + str(dst_ping["DURING"][i]) + "\n")
					# After failure
					file.write("\tAfter failure:\n")
					file.write("\t\t" + str(dst_ping["AFTER"][i]) + "\n")
			if ifRouted == True:
				file.write("Failure: %s:%s -> %s:%s @ %f - %f\n\n"%(router1, port1, router2, port2, failure_start, failure_end))
		print(self.ipcounter)

fd = FailureDetection()
fd.lookUp()
