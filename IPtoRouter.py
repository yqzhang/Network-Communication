class Router:
	router = ""
	port = ""
	valid_till = 0
	
	def __init__(self, router, port, valid_till):
		self.router = router
		self.port = port
		self.valid_till = valid_till
	
class IP:
	IP = ""
	valid_till = 0
	
	def __init__(self, IP, valid_till):
		self.IP = IP
		self.valid_till = valid_till

class ISISRouter:
	IPtoRouter = {}
	RoutertoIP = {}

	def __init__(self, filename):
		# Parse the data from file
		file = open(filename)
		count = 0
		for line in file:
			if line[0] != '#':
				count++
				data = line.split(",")
				insert(data[0], data[1], data[2], data[3])
		print("%d lines inserted."%count)
	
	def __del__(self):
		# TODO: Nothing
		pass
		
	def insert(ip_address, router, port, valid_till):
		# Insert data into the table
		if IPtoRouter.has_key(ip_address):
			list = IPtoRouter[ip_address]
			for i in xrange(len(list)):
				if list[i].valid_till > valid_till:
					list.insert(i, Router(router, port, valid_till))
					break
			else:
				list.append(Router(router, port, valid_till))
		else:
			IPtoRouter[ip_address] = [Router(router, port, valid_till)]
		
		if RoutertoIP.has_key(router + ":" + port):
			list = RoutertoIP[router + ":" + port]
			for i in xrange(len(list)):
				if list[i].valid_till > valid_till:
					list.insert(i, IP(ip_address, valid_till))
					break
			else:
				list.append(IP(ip_address, valid_till))
		else:
			RoutertoIP[router + ":" + port] = [IP(ip_address, valid_till)]
		
	def delete(ip_address, router, port, valid_till):
		# Delete certain data from the table
		
	def update(ip_address, router, port, valid_till):
		# Update certain data in the table
		
	def query_by_ip(ip_address, time):
		# Query by IP address and timestamp
		# Return router and port
		if IPtoRouter.has_key(ip_address):
			for router in IPtoRouter[ip_address]:
				if time <= router.valid_till:
					return router
			else:
				return NULL
		else:
			return NULL
		
	def query_by_router(router, port, time):
		# Query by router, port and time
		# Return IP address
		if RoutertoIP.has_key(router + ":" + port):
			for ip in RoutertoIP[router + ":" + port]:
				if time <= ip.valid_till:
					return ip.IP
			else:
				return NULL
		else:
			return NULL
		