#!/usr/bin/env python
# Author: Yunqi Zhang
# Email: yqzhang@ucsd.edu

import LinkMap
import FailureVerifier
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
	linkmap = LinkMap.LinkMap()
	failureVerifier = FailureVerifier.PingFailureVerifier()

	# Source ID Map for ping data
	SourceIDMap = {'ucsb':0,'ucla':1,'ucsd':2,'ucdavis':3,'berkeley':4,'ucsc':5}

	def __init__(self):
		# Initiate the failure list from ISISFailure.py
		# Format: router1, port1, router2, port2, failure_start, failure_end
		self.failureList = ISISFailure().traverse()
		# Initiate Utils
		self.util.ReadFormatedPingDataIntoMemory()

	def lookUpByIP(self, IP, failure_start, failure_end, destination):
		# Look up the ping data from Utils.py
		# Search by IP address
		retval = dict()

		# @parameter: destination determines whether to look up for destination or last hop
		# True for destination, False for last hop
		if destination == True:
			query_method = 0
		else:
			query_method = 1

		for i in range(6):
			ifBefore = True
			preData = None
			retval[i] = list()

			# Search by the last hop
			for ip in IP:
				for data in self.util.FindPing(i, ip, query_method):
					if data[1] < failure_start:
						# Before
						preData = data
					elif data[0] > failure_start and data[0] < (failure_end + 30.0) and ifBefore == True:
						# During
						if preData != None:
							retval[i].append(preData)
						retval[i].append(data)
						ifBefore = False
					elif data[0] > (failure_end + 100.0):
						# After
						break
					else:
						# During
						retval[i].append(data)

		return retval

	def lookUpByRouter(self, router, port, failure_start, failure_end, ifPort, ip):
		ip_list = []
		#Convert router:port to IP and call lookUpByIP()
		ip.append(self.iprouter.query_by_router(router, port, failure_start))
		if ifPort == True:
			ip_list.append(self.iprouter.query_by_router(router, port, failure_start))
		else:
			ip_list = self.iprouter.query_without_port(router, failure_start)

		if ip_list == None:
			#print("No IP addresses assigned T_T")
			return None
		else:
			#print(ip_list)
			#print(failure_start)
			#print(failure_end)
			if ifPort == True:
				return self.lookUpByIP(ip_list, failure_start, failure_end, False)
			else:
				return self.lookUpByIP(ip_list, failure_start, failure_end, True)

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
		# Output in xml format
		file = open("route_change.xml", "w")

		# Statistics
		failure_count = 0
		map_count = 0
		no_ip_count = 0
		non_reachable_count = 0
		question_count = 0
		both_count = 0

		# Traverse the failure list and look them up
		for fail in self.failureList:
			# Statistics
			failure_count += 1
			if fail[1] == "??" or fail[3] == "??":
				question_count += 1

			router1 = fail[0]
			port1 = fail[1]
			router2 = fail[2]
			port2 = fail[3]
			failure_start = float(fail[4])
			failure_end = float(fail[5])

			src_ip = list()
			dst_ip = list()
			# Format: router1, port1, router2, port2, failure_start, failure_end
			src_ping = self.lookUpByRouter(router1, port1, failure_start, failure_end, False, src_ip)
			dst_ping = self.lookUpByRouter(router2, port2, failure_start, failure_end, False, dst_ip)

			output_buffer = "<Failure>\n\t<Source>" + router1 + ":" + port1 + "</source>\n"
			output_buffer += "\t<destination>" + router2 + ":" + port2 + "</destination>\n"
			output_buffer += "\t<src_ip>" + str(src_ip[0]) + "</src_ip>\n"
			output_buffer += "\t<dst_ip>" + str(dst_ip[0]) + "</dst_ip>\n"
			output_buffer += "\t<start>" + str(failure_start) + "</start>\n"
			output_buffer += "\t<end>" + str(failure_end) + "</end>\n"

			if src_ping == None and dst_ping == None:
				no_ip_count += 1
				continue

			ifRouted = False
			ifReachable = True
			ifSrc = False
			ifDes = False
			for i in range(6):
				output_buffer += "\t<source id=\"" + str(i) + "\">\n"
				if src_ping != None and src_ping[i] != None and self.ifChanged(src_ping[i]) == True:
					ifRouted = True
					ifSrc = True
					output_buffer += "\t\t<to=source>\n"
					for ping in src_ping[i]:
						if ping[0] < failure_start:
							output_buffer += "\t\t\t<before>" + str(ping[2]) + ", " + str(ping[3]) + ", " + str(ping[4]) + "</before>\n"
						elif ping[0] < failure_end:
							output_buffer += "\t\t\t<during>" + str(ping[2]) + ", " + str(ping[3]) + ", " + str(ping[4]) + "</during>\n"
						else:
							output_buffer += "\t\t\t<after>" + str(ping[2]) + ", " + str(ping[3]) + ", " + str(ping[4]) + "</after>\n"
						if ping[3] == False:
							ifReachable = False
					output_buffer += "\t\t</to>\n"

				if dst_ping != None and dst_ping[i] != None and self.ifChanged(dst_ping[i]) == True:
					ifRouted = True
					ifDes = True
					output_buffer += "\t\t<to=destination>\n"
					for ping in dst_ping[i]:
						if ping[0] < failure_start:
							output_buffer += "\t\t\t<before>" + str(ping[2]) + ", " + str(ping[3]) + ", " + str(ping[4]) + "</before>\n"
						elif ping[0] < failure_end:
							output_buffer += "\t\t\t<during>" + str(ping[2]) + ", " + str(ping[3]) + ", " + str(ping[4]) + "</during>\n"
						else:
							output_buffer += "\t\t\t<after>" + str(ping[2]) + ", " + str(ping[3]) + ", " + str(ping[4]) + "</after>\n"
						if ping[3] == False:
							ifReachable = False
					output_buffer += "\t\t</to>\n"
				output_buffer += "\t</source>\n"
			output_buffer += "</Failure>\n"
			if ifReachable == False:
				non_reachable_count += 1
			if ifRouted == True:
				map_count += 1
				file.write(output_buffer)
			if ifSrc == True and ifDes == True:
				both_count += 1
		# Statistics
		print("------------------------------STATISTICS---------------------------------")
		print("Total failure: %d" %failure_count)
		print("Mapped failure count: %d" %map_count)
		print("No IP address: %d" %no_ip_count)
		print("Caused inreachable: %d" %non_reachable_count)
		print("Question port: %d" %question_count)
		print("Both end nodes have been pinged: %d" %both_count)

	def analyzeFailureToRoute(self):
		# Output file "route_change.xml"
		# Output in xml format
		file = open("route_change_with_weight.xml", "w")

		# Statistics
		failure_count = 0
		map_count = 0
		no_ip_count = 0
		non_reachable_count = 0
		question_count = 0
		both_count = 0

		# Traverse the failure list and look them up
		for fail in self.failureList:
			# Statistics
			failure_count += 1
			if fail[1] == "??" or fail[3] == "??":
				question_count += 1

			router1 = fail[0]
			port1 = fail[1]
			router2 = fail[2]
			port2 = fail[3]
			failure_start = float(fail[4])
			failure_end = float(fail[5])

			src_ip = list()
			dst_ip = list()
			# Format: router1, port1, router2, port2, failure_start, failure_end
			src_ping = self.lookUpByRouter(router1, port1, failure_start, failure_end, False, src_ip)
			dst_ping = self.lookUpByRouter(router2, port2, failure_start, failure_end, False, dst_ip)

			output_buffer = "<Failure>\n\t<Source>" + router1 + ":" + port1 + "</source>\n"
			output_buffer += "\t<destination>" + router2 + ":" + port2 + "</destination>\n"
			output_buffer += "\t<src_ip>" + str(src_ip[0]) + "</src_ip>\n"
			output_buffer += "\t<dst_ip>" + str(dst_ip[0]) + "</dst_ip>\n"
			output_buffer += "\t<start>" + str(failure_start) + "</start>\n"
			output_buffer += "\t<end>" + str(failure_end) + "</end>\n"

			if src_ping == None and dst_ping == None:
				no_ip_count += 1
				continue

			ifRouted = False
			ifReachable = True
			ifSrc = False
			ifDes = False
			for i in range(6):
				output_buffer += "\t<source id=\"" + str(i) + "\">\n"
				if src_ping != None and src_ping[i] != None and self.ifChanged(src_ping[i]) == True:
					ifRouted = True
					ifSrc = True
					output_buffer += "\t\t<to=source>\n"
					withFailLink = 0
					withoutFailLink = 0
					for ping in src_ping[i]:
						routerPath = self.failureVerifier.getPath(ping)
						if ping[0] < failure_start:
							output_buffer += "\t\t\t<before>" + str(ping[2]) +", "+ str(self.linkmap.calWeight(routerPath)) + ", "+ str(ping[3]) + ", " + str(routerPath ) + "</before>\n"
						elif ping[0] < failure_end:
							output_buffer += "\t\t\t<during>" + str(ping[2]) + ", " + str(self.linkmap.calWeight(routerPath)) + ", " + str(ping[3]) + ", " + str(routerPath) + "</during>\n"
							for k in range(len(routerPath)-1):
								if (routerPath[k],routerPath[k+1]) == (router1,router2)	or (routerPath[k],routerPath[k+1]) == (router2,router1):
									withFailLink += 1
								else:
									withoutFailLink += 1
						else:
							output_buffer += "\t\t\t<after>" + str(ping[2]) + ", " + str(self.linkmap.calWeight(routerPath)) + ", " + str(ping[3]) + ", " + str(routerPath) + "</after>\n"
						if ping[3] == False:
							ifReachable = False
					output_buffer += "\t\t</to>\n"
					output_buffer += "<Analyze>total:"+str(len(src_ping))+", withlink:"+str(withFailLink)+", withoutFailLink:"+str(withoutFailLink)+"</Analyze>\n"

				if dst_ping != None and dst_ping[i] != None and self.ifChanged(dst_ping[i]) == True:
					ifRouted = True
					ifDes = True
					output_buffer += "\t\t<to=destination>\n"
					withFailLink = 0
					withoutFailLink = 0
					for ping in dst_ping[i]:
						routerPath = self.failureVerifier.getPath(ping)
						if ping[0] < failure_start:
							output_buffer += "\t\t\t<before>" + str(ping[2]) + ", "+ str(self.linkmap.calWeight(routerPath)) + ", "+ str(ping[3]) + ", " + str(routerPath) + "</before>\n"
						elif ping[0] < failure_end:
							output_buffer += "\t\t\t<during>" + str(ping[2]) + ", " + str(self.linkmap.calWeight(routerPath)) + ", " + str(ping[3]) + ", " + str(routerPath) + "</during>\n"
							for k in range(len(routerPath)-1):
								if (routerPath[k],routerPath[k+1]) == (router1,router2)	or (routerPath[k],routerPath[k+1]) == (router2,router1):
									withFailLink += 1
								else:
									withoutFailLink += 1
						else:
							output_buffer += "\t\t\t<after>" + str(ping[2]) + ", " + str(self.linkmap.calWeight(routerPath)) + ", " + str(ping[3]) + ", " + str(routerPath) + "</after>\n"
						if ping[3] == False:
							ifReachable = False
					output_buffer += "\t\t</to>\n"
					output_buffer +=\
					"<Analyze>total:"+str(len(dst_ping))+",	withlink:"+str(withFailLink)+",	withoutFailLink:"+str(withoutFailLink)+"</Analyze>\n"
				output_buffer += "\t</source>\n"
			output_buffer += "</Failure>\n"
			if ifReachable == False:
				non_reachable_count += 1
			if ifRouted == True:
				map_count += 1
				file.write(output_buffer)
			if ifSrc == True and ifDes == True:
				both_count += 1
		# Statistics
		print("------------------------------STATISTICS---------------------------------")
		print("Total failure: %d" %failure_count)
		print("Mapped failure count: %d" %map_count)
		print("No IP address: %d" %no_ip_count)
		print("Caused inreachable: %d" %non_reachable_count)
		print("Question port: %d" %question_count)
		print("Both end nodes have been pinged: %d" %both_count)

	def failurePlot(self):
		# Output to failure_plot.data
		plot = open("failure_plot.data", "w")
		output_buffer = ""
		count = 0
		# Traverse the failure list and look them up
		for fail in self.failureList:
			router1 = fail[0]
			port1 = fail[1]
			router2 = fail[2]
			port2 = fail[3]
			failure_start = float(fail[4])
			failure_end = float(fail[5])
			src_ip = list()
			dst_ip = list()
			# Format: router1, port1, router2, port2, failure_start, failure_end
			src_ping = self.lookUpByRouter(router1, port1, failure_start, failure_end, False, src_ip)
			dst_ping = self.lookUpByRouter(router2, port2, failure_start, failure_end, False, dst_ip)

			for i in range(6):
				if src_ping != None and src_ping[i] != None and self.ifChanged(src_ping[i]) == True:
					count += 1
					before = after = "NaN"
					ifDuring = False
					for ping in src_ping[i]:
						if ping[0] < failure_start:
							if ping[3] == True:
								before = str(count)
							else:
								before = "NaN"
						elif ping[0] < failure_end:
							if ifDuring == False:
								output_buffer += "0\t" + str(before) + "\n"
								ifDuring = True
							output_buffer += str((ping[0] - failure_start) / (failure_end - failure_start) * 100) + "\t"
							if ping[3] == True:
								output_buffer += str(count) + "\n"
							else:
								output_buffer += "NaN\n"
						else:
							if ifDuring == False:
								output_buffer += "0\t" + str(before) + "\n"
								ifDuring = True
							output_buffer += str(ping[0] - failure_start) + "\t"
							if ping[3] == True:
								output_buffer += str(count)
							else:
								output_buffer += "NaN\n"
							break
					output_buffer += "\n"
				if dst_ping != None and dst_ping[i] != None and self.ifChanged(dst_ping[i]) == True:
					count += 1
					before = after = "NaN"
					ifDuring = False
					for ping in dst_ping[i]:
						if ping[0] < failure_start:
							if ping[3] == True:
								before = str(count)
							else:
								before = "NaN"
						elif ping[0] < failure_end:
							if ifDuring == False:
								output_buffer += "0\t" + str(before) + "\n"
								ifDuring = True
							output_buffer += str(ping[0] - failure_start) + "\t"
							if ping[3] == True:
								output_buffer += str(count) + "\n"
							else:
								output_buffer += "NaN\n"
						else:
							if ifDuring == False:
								output_buffer += "0\t" + str(before) + "\n"
								ifDuring = True
							output_buffer += str(ping[0] - failure_start) + "\t"
							if ping[3] == True:
								output_buffer += str(count)
							else:
								output_buffer += "NaN\n"
							break
					output_buffer += "\n"
		plot.write(output_buffer)

	def failureRecovery(self):
		# Output to failure_plot.data
		plot = open("../plot/failure_time.dat", "w")
		output_buffer = ""
		prob = [0] * 1000
		count = 0
		accum = 0
		# Traverse the failure list and look them up
		for fail in self.failureList:
			count += 1
			failure_start = float(fail[4])
			failure_end = float(fail[5])
			if failure_end - failure_start < 1000:
				prob[int(failure_end - failure_start)] += 1
			#output_buffer += str((failure_end - failure_start) / 60) + "\n"
		for i in range(1000):
			accum += prob[i]
			output_buffer += str(i) + "\t" + str(float(accum) / count) + "\n"
		plot.write(output_buffer)

	def accessibilityPlot(self):
		plot = open("../plot/accessibility.dat", "w")
		output_buffer = ""
		prob = [0] * 10001
		count = 0
		for fail in self.failureList:
			router1 = fail[0]
			port1 = fail[1]
			router2 = fail[2]
			port2 = fail[3]
			failure_start = float(fail[4])
			failure_end = float(fail[5])
			src_ip = list()
			dst_ip = list()
			# Format: router1, port1, router2, port2, failure_start, failure_end
			src_ping = self.lookUpByRouter(router1, port1, failure_start, failure_end, False, src_ip)
			dst_ping = self.lookUpByRouter(router2, port2, failure_start, failure_end, False, dst_ip)

			for i in range(6):
				if src_ping != None and src_ping[i] != None and self.ifChanged(src_ping[i]) == True:
					count += 1
					total = access = 0
					for ping in src_ping[i]:
						if ping[0] >= failure_start - 30.0 and ping[0] < failure_end + 100.0:
							total += 1
							if ping[3] == True:
								access += 1
					if access == 0:
						prob[0] += 1
					else:
						prob[int(float(access) / float(total * 10000))] += 1
				if dst_ping != None and dst_ping[i] != None and self.ifChanged(dst_ping[i]) == True:
					count += 1
					total = access = 0
					for ping in dst_ping[i]:
						if ping[0] >= failure_start and ping[0] < failure_end:
							total += 1
							if ping[3] == True:
								access += 1
					if access == 0:
						prob[0] += 1
					else:
						prob[int(float(access) / float(total) * 10000)] += 1
		accum = 0
		print(count)
		for i in range(10001):
			accum += prob[i]
			output_buffer += str(i) + "\t" + str(float(accum) / count) + "\n"
		plot.write(output_buffer)

fd = FailureDetection()
fd.analyzeFailureToRoute()
