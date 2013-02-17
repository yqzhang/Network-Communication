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
				if num_lines < 5:
					print (arr[0], arr[1]), (arr[2], arr[3]), self.link_list[(arr[0], arr[1])][(arr[2], arr[3])]

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

	def hasLink(self, router1, port1, router2, port2, timestamp):
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

	def getLinks(self, router, port, timestamp):
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


path = "links_new_format.txt"
lm = LinkMap(path)  ##generate a link map from given file..
print lm.hasLink('bak-agg2','GigabitEthernet0/0/7','ker-cc-1','GigabitEthernet0/1', 12155907889) ##just return a boolean...
print lm.getLinks('bak-agg2','GigabitEthernet0/0/7', 1215590788)  ##return a dictionary with key = (router2, port2) and val = [(time_create, time_destroy)] Generally val should be a list containing only one element, but I'm not quite sure...
