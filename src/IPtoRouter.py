#!/usr/bin/env python
# Author: Yunqi Zhang
# Email: yqzhang@ucsd.edu

import os

# Describe the routers
class Router:
	router = ""
	port = ""
	valid_till = 0.0
	
	def __init__(self, router, port, valid_till):
		self.router = router
		self.port = port
		self.valid_till = valid_till
	
# Describe the IP addresses
class IP:
	IP = ""
	valid_till = 0.0
	
	def __init__(self, IP, valid_till):
		self.IP = IP
		self.valid_till = valid_till
	
# Describe the map between IP addresses and routers
class IPRouter:
	IPtoRouter = dict()
	RoutertoIP = dict()
	RoutertoPort = dict()

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
			line = line.strip()
			if line[0] != '#':
				count += 1
				data = line.split(",")
				self.insert(data[0], data[1], data[2], float(data[3]))
		self.sort()
		print("%d lines inserted from file %s. [output from IPtoRouter.py]"%(count, filename))
	
	def sort(self):
		# Sort the maps by valid_till
		for key, value in self.IPtoRouter.items():
			value = sorted(value, key = lambda router: router.valid_till)
		
		for key, value in self.RoutertoIP.items():
			value = sorted(value, key = lambda ip: ip.valid_till)
		
		for key, value in self.RoutertoPort.items():
			for k, v in value.items():
				v = sorted(v, key = lambda ip: ip.valid_till)
	
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
		
		if router in self.RoutertoPort:
			if port in self.RoutertoPort[router]:
				self.RoutertoPort[router][port].append(IP(ip_address, valid_till))
			else:
				self.RoutertoPort[router][port] = []
				self.RoutertoPort[router][port].append(IP(ip_address, valid_till))
		else:
			self.RoutertoPort[router] = dict()
			self.RoutertoPort[router][port] = []
			self.RoutertoPort[router][port].append(IP(ip_address, valid_till))
		
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
				return None
		else:
			return None
		
	def query_by_router(self, router, port, time):
		# Query by router, port and time
		# Return IP address
		if (router + ":" + port) in self.RoutertoIP:
			for ip in self.RoutertoIP[router + ":" + port]:
				if time <= ip.valid_till:
					return ip.IP
			else:
				return None
		else:
			return None
	
	def query_without_port(self, router, time):
		# Query by router and time without port
		# Return a list of IP addresses
		if router in self.RoutertoPort:
			retval = []
			for key, value in self.RoutertoPort[router].items():
				# print(value)
				for ip in value:
					if time <= ip.valid_till:
						retval.append(ip.IP)
						break
		else:
			return None
		
		if len(retval) == 0:
			return None
		else:
			return retval
	
# For test
# r = IPRouter("C:\\Users\\Del\\Desktop\\ipToRouters.txt")
# r = IPRouter()
# print(r.query_without_port("cyp-6509-msfc", 253402300797))
# print(r.query_by_router("cyp-6509-msfc", "Vlan851", 253402300797))
