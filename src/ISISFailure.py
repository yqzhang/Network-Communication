#!/usr/bin/env python
# Author: Yunqi Zhang
# Email: yqzhang@ucsd.edu

import os

# Describe the Failure
class Failure:
	router = ""
	port = ""
	failure_start = 0.0
	failure_end = 0.0

	def __init__(self, router, port, failure_start, failure_end):
		self.router = router
		self.port = port
		self.failure_start = failure_start
		self.failure_end = failure_end

# Describe the ISISFailure
class ISISFailure:
	failureMap = dict()
	failureList = list()

	def __init__(self, filename = "../data/isis_failures/isis_fails_2012-11-01--2013_02_07.txt"):
		# Parse the data from file
		parentDir = os.path.dirname(os.getcwd())
		self.append(parentDir + filename[2:])

	def __del__(self):
		# TODO: Nothing
		pass

	def append(self, filename):
		# Append the map from raw data
		file = open(filename)
		count = 0
		for line in file:
			line = line.strip()
			if line[0] != "#":
				count += 1
				data = line.split(",")
				self.insert(data[0], data[1], data[2], data[3], float(data[4]), float(data[5]))
		self.sort()
		print("%d lines inserted from file %s. [output from ISISFailure.py]"%(count, filename))

	def sort(self):
		# Sort the data by failure start time
		for k, v in self.failureMap.items():
			for key, value in v.items():
				value = sorted(value, key = lambda failure: failure.failure_start)

	def insert(self, router1, port1, router2, port2, failure_start, failure_end):
		# Insert data into the map[router1]
		if router1 in self.failureMap:
			routerMap = self.failureMap[router1]
			if port1 in routerMap:
				list = routerMap[port1]
				list.append(Failure(router2, port2, failure_start, failure_end))
			else:
				routerMap[port1] = [Failure(router2, port2, failure_start, failure_end)]
		else:
			routerMap = {}
			routerMap[port1] = [Failure(router2, port2, failure_start, failure_end)]
			self.failureMap[router1] = routerMap

		# Insert data into the map[router2]
		if router2 in self.failureMap:
			routerMap = self.failureMap[router2]
			if port2 in routerMap:
				list = routerMap[port2]
				list.append(Failure(router1, port1, failure_start, failure_end))
			else:
				routerMap[port2] = [Failure(router1, port1, failure_start, failure_end)]
		else:
			routerMap = {}
			routerMap[port2] = [Failure(router1, port1, failure_start, failure_end)]
			self.failureMap[router2] = routerMap

		# Insert data into the list
		temp = [router1, port1, router2, port2, failure_start, failure_end]
		self.failureList.append(temp)

	def delete(self, router1, port1, router2, port2, failure_start, failure_end):
		# Delete certain data from the map
		pass

	def update(self, router1, port1, router2, port2, failure_start, failure_end):
		# Update certain data in the map
		pass

	def query_by_router(self, router):
		if router in self.failureMap:
			return self.failureMap[router]
		else:
			return None

	def query_by_router_port(self, router,port):
		if router in self.failureMap:
			routerMap = self.failureMap[router]
			if port in routerMap:
				return routerMap[port]
			else:
				return None
		else:
			return None

	def traverse(self):
		return self.failureList


# For test
# f = ISISFailure()
# failures = f.query_by_router_port("lax-dc2", "GigabitEthernet4/0/7")
# for ite in failures:
#	print("%s %s %d %d" % (ite.router, ite.port, ite.failure_start, ite.failure_end))
