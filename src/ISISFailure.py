#!/usr/bin/env python
# Author: Yunqi Zhang
# Email: yqzhang@ucsd.edu

# Describe the Failure
class Failure:
	router = ""
	port = ""
	failure_start = 0
	failure_end = 0
	
	def __init__(self, router, port, failure_start, failure_end):
		self.router = router
		self.port = port
		self.failure_start = failure_start
		self.failure_end = failure_end

# Describe the ISISFailure
class ISISFailure:
	failureMap = {}
	
	def __init__(self, filename):
		# Parse the data from file
		file = open(filename)
		count = 0
		for line in file:
			if line[0] != '#':
				count += 1
				data = line.split(",")
				self.insert(data[0], data[1], data[2], data[3], int(data[4][:-3]), int(data[5][:-3]))
		print("%d lines inserted."%count)
		
	def __del__(self):
		# TODO: Nothing
		pass
		
	def insert(self, router1, port1, router2, port2, failure_start, failure_end):
		# Insert data into the map[router1]
		if router1 in self.failureMap:
			routerMap = self.failureMap[router1]
			if port1 in routerMap:
				list = routerMap[port1]
				for i in range(len(list)):
					if list[i].failure_start > failure_start:
						list.insert(i, Failure(router2, port2, failure_start, failure_end))
						break
				else:
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
				for i in range(len(list)):
					if list[i].failure_start > failure_start:
						list.insert(i, Failure(router1, port1, failure_start, failure_end))
						break
				else:
					list.append(Failure(router1, port1, failure_start, failure_end))
			else:
				routerMap[port2] = [Failure(router1, port1, failure_start, failure_end)]
		else:
			routerMap = {}
			routerMap[port2] = [Failure(router1, port1, failure_start, failure_end)]
			self.failureMap[router2] = routerMap
	
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
			return NULL
		
	def query_by_router_port(self, router,port):
		if router in self.failureMap:
			routerMap = self.failureMap[router]
			if port in routerMap:
				return routerMap[port]
			else:
				return NULL
		else:
			return NULL
		
# For test
# f = ISISFailure("C:\\Users\\Del\\Desktop\\isis_failures_old.txt")
# failures = f.query_by_router_port("lax-dc2", "GigabitEthernet4/0/7")
# for ite in failures:
# 	print("%s %s %d %d" % (ite.router, ite.port, ite.failure_start, ite.failure_end))
