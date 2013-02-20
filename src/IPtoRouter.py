#!/usr/bin/env python
# Author: Yunqi Zhang
# Email: yqzhang@ucsd.edu

import os

# Describe the routers
class Router:
	router = ""
	port = ""
	valid_till = 0
	
	def __init__(self, router, port, valid_till):
		self.router = router
		self.port = port
		self.valid_till = int(valid_till)
	
# Describe the IP addresses
class IP:
	IP = ""
	valid_till = 0
	
	def __init__(self, IP, valid_till):
		self.IP = IP
		self.valid_till = int(valid_till)
	
# Describe the map between IP addresses and routers
class IPRouter:
	IPtoRouter = dict()
	RoutertoIP = dict()

	def __init__(self, filename = "../data/maps/ipToRouters.txt"):
		# Parse the data from file
		parentDir = os.path.dirname(os.getcwd())
		self.append(parentDir + filename[2:])
	
	def __del__(self):
		# TODO: Nothing
		pass
	
	def append(self, filename):
		# Append the maps from raw data
		file = open(filename)
		count = 0
		for line in file:
			if line[0] != '#':
				count += 1
				data = line[:-1].split(",")
				self.insert(data[0], data[1], data[2], int(data[3]))
		self.sort()
		print("%d lines inserted."%count)
	
	def sort(self):
		# Sort the maps by valid_till
		for key, value in self.IPtoRouter.items():
			value = sorted(value, key = lambda router: router.valid_till)
		
		for key, value in self.RoutertoIP.items():
			value = sorted(value, key = lambda ip: ip.valid_till)
	
	def insert(self, ip_address, router, port, valid_till):
		# Insert data into the table
		if ip_address in self.IPtoRouter:
			list = self.IPtoRouter[ip_address]
			list.append(Router(router, port, valid_till))
		else:
			self.IPtoRouter[ip_address] = [Router(router, port, valid_till)]
		
		if router + ":" + port in self.RoutertoIP:
			list = self.RoutertoIP[router + ":" + port]
			list.append(IP(ip_address, valid_till))
		else:
			self.RoutertoIP[router + ":" + port] = [IP(ip_address, valid_till)]
		
	def delete(self, ip_address, router, port, valid_till):
		# Delete certain data from the table
		pass
		
	def update(self, ip_address, router, port, valid_till):
		# Update certain data in the table
		pass
		
	def query_by_ip(self, ip_address, time):
		# Query by IP address and timestamp
		# Return router and port
		if ip_address in self.IPtoRouter:
			for router in self.IPtoRouter[ip_address]:
				if time <= router.valid_till:
					return router
			else:
				return NULL
		else:
			return NULL
		
	def query_by_router(self, router, port, time):
		# Query by router, port and time
		# Return IP address
		if (router + ":" + port) in self.RoutertoIP:
			for ip in self.RoutertoIP[router + ":" + port]:
				if time <= ip.valid_till:
					return ip.IP
			else:
				return NULL
		else:
			return NULL
		
# For test
# r = IPRouter("C:\\Users\\Del\\Desktop\\ipToRouters.txt")
# r = IPRouter()
# print(r.query_by_ip("137.164.80.1", 253402300797).router)
# print(r.query_by_router("cyp-6509-msfc", "Vlan851", 253402300797))
