class LinkMap:
	link_list = {}
	def __init__(self, path):
		f = open(path, "r")
		self.link_list = {}
		num_lines = 0
		for line in f:
			num_lines += 1
			if num_lines > 2:
				arr = line.split(',')
				self.addLink(arr[0], arr[1], arr[2], arr[3], float(arr[4]), float(arr[5].strip()))
				self.addLink(arr[2], arr[3], arr[0], arr[1], float(arr[4]), float(arr[5].strip()))

	def __del__(self):
		del self.link_list

	def addLink(self, router1, port1, router2, port2, time_create, time_destroy):
		key1 = (router1, port1)
		key2 = (router2, port2)
		val = (time_create, time_destroy)
		if key1 in self.link_list:
			if key2 in self.link_list[key1]:
				self.link_list[key1][key2].append(val)
			else:
				self.link_list[key1][key2] = [val]
		else:
			self.link_list[key1] = {key2:[val]}

	def hasLink1(self, router1, port1, router2, port2, timestamp):
		key1 = (router1, port1)
		key2 = (router2, port2)
		if key1 in self.link_list:
			if key2 in self.link_list[key1]:
				timerange_list = self.link_list[key1][key2]
				for timerange in timerange_list:
					if timestamp > timerange[0] and timestamp < timerange[1]:
						return True
		if key2 in self.link_list:
			if key1 in self.link_list[key2]:
				timerange_list = self.link_list[key2][key1]
				for timerange in timerange_list:
					if timestamp > timerange[0] and timestamp < timerange[1]:
						return True
		return False

	def hasLink2(self, router1, port1, router2, port2, time_start, time_end):
		key1 = (router1, port1)
		key2 = (router2, port2)
		if key1 in self.link_list:
			if key2 in self.link_list[key1]:
				timerange_list = self.link_list[key1][key2]
				for timerange in timerange_list:
					if time_start > timerange[0] and time_end < timerange[1]:
						return True
		if key2 in self.link_list:
			if key1 in self.link_list[key2]:
				timerange_list = self.link_list[key2][key1]
				for timerange in timerange_list:
					if time_start > timerange[0] and time_end < timerange[1]:
						return True
		return False

	def getLinks1(self, router, port, timestamp):
		temp_link_list = {}
		key = (router, port)
		if key in self.link_list:
			for item in self.link_list[key]:
				hasLink = False
				for timerange in self.link_list[key][item]:
					if timestamp > timerange[0] and timestamp < timerange[1]:
						if hasLink:
							temp_link_list[item].append(timerange)
						else:
							temp_link_list[item] = [timerange]
		return temp_link_list

	def getLinks2(self, router, port, time_start, time_end):
		temp_link_list = {}
		key = (router, port)
		if key in self.link_list:
			for item in self.link_list[key]:
				hasLink = False
				for timerange in self.link_list[key][item]:
					if time_start > timerange[0] and time_end < timerange[1]:
						if hasLink:
							temp_link_list[item].append(timerange)
						else:
							temp_link_list[item] = [timerange]
		return temp_link_list

	def getValidTime(self, router1, port1, router2, port2):
		key1 = (router1, port1)
		key2 = (router2, port2)
		if key1 in self.link_list and key2 in self.link_list[key1]:
			return self.link_list[key1][key2]
		return None
