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
		
		for i in range(6):
			ifBefore = True
			preData = None
			retval[i] = list()
			
			# Search by the last hop
			for data in self.util.FindPing(i, IP, 1):
				if data[1] < failure_start:
					# Before
					preData = data
				elif data[0] > failure_start and data[0] < (failure_end + 30.0) and ifBefore == True:
					# During
					if preData != None:
						retval[i].append(preData)
					retval[i].append(data)
					ifBefore = False
				elif data[0] > (failure_end + 30.0):
					# After
					break
				else:
					# During
					retval[i].append(data)

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

	def diff(self, list_1, list_2):
		if len(list_1) != len(list_2):
			return True
		else:
			i = 0
			length = len(list_1)
			while i < length:
				if list_1[i] != list_2[i]:
					return True
				i += 1
			return False
	
	def removeAll_list(self, l, item):
		while item in l:
			l.remove(item)
	
	def diffWithStars(self, list_1, list_2):
		self.removeAll_list(list_1, "* *")
		self.removeAll_list(list_2, "* *")
		return self.diff(list_1, list_2)
	
	def ifChanged(self, ping_list):
		length = len(ping_list)
		#print("length: %d"%length)
		for i in range(length - 1):
			if self.diff(ping_list[i][4], ping_list[i + 1][4]) == True:
				return True
		else:
			return False
			
	def lookUp(self):
		# Output file "route_change.xml"
		file = open("route_change.xml", "w")
	
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
			
			output_buffer = "<Failure>\n\t<Source>" + router1 + ":" + port1 + "</source>\n"
			output_buffer += "\t<destination>" + router2 + ":" + port2 + "</destination>\n"
			output_buffer += "\t<start>" + str(failure_start) + "</start>\n"
			output_buffer += "\t<end>" + str(failure_end) + "</end>\n"
			
			if src_ping == None and dst_ping == None:
				continue

			ifRouted = False
			for i in range(6):
				output_buffer += "\t<source id=" + str(i) + ">\n"
				if src_ping != None and src_ping[i] != None and self.ifChanged(src_ping[i]) == True:
					ifRouted = True
					output_buffer += "\t\t<to=source>\n"
					for ping in src_ping[i]:
						output_buffer += "\t\t\t<ping>" + str(ping) + "</ping>\n"
					output_buffer += "\t\t</to>\n"
					
				if dst_ping != None and dst_ping[i] != None and self.ifChanged(dst_ping[i]) == True:
					ifRouted = True
					output_buffer += "\t\t<to=destination>\n"
					for ping in dst_ping[i]:
						output_buffer += "\t\t\t<ping>" + str(ping) + "</ping>\n"
					output_buffer += "\t\t</to>\n"
				output_buffer += "\t</source id=" + str(i) + ">\n"
			output_buffer += "</Failure>\n"
			if ifRouted == True:
				file.write(output_buffer)
		print(self.ipcounter)

fd = FailureDetection()
fd.lookUp()
