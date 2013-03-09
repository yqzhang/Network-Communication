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
				self.addLink(arr[0], arr[2], float(arr[4]), float(arr[5].strip()))
				self.addLink(arr[2], arr[0], float(arr[4]), float(arr[5].strip()))

	def __del__(self):
		del self.link_list

	def addLink(self, router1, router2, time_create, time_destroy):
		val = (time_create, time_destroy)
		if router1 in self.link_list:
			if router2 in self.link_list[router1]:
				self.link_list[router1][router2].append(val)
			else:
				self.link_list[router1][router2] = [val]
		else:
			self.link_list[router1] = {router2:[val]}

	def hasLink1(self, router1, router2, timestamp):
		if router1 in self.link_list:
			if router2 in self.link_list[router1]:
				timerange_list = self.link_list[router1][router2]
				for timerange in timerange_list:
					if timestamp > timerange[0] and timestamp < timerange[1]:
						return True
		if router2 in self.link_list:
			if router1 in self.link_list[router2]:
				timerange_list = self.link_list[router2][router1]
				for timerange in timerange_list:
					if timestamp > timerange[0] and timestamp < timerange[1]:
						return True
		return False

	def hasLink2(self, router1, router2, time_start, time_end):
		if router1 in self.link_list:
			if router2 in self.link_list[router1]:
				timerange_list = self.link_list[router1][router2]
				for timerange in timerange_list:
					if time_start > timerange[0] and time_end < timerange[1]:
						return True
		if router2 in self.link_list:
			if router1 in self.link_list[router2]:
				timerange_list = self.link_list[router2][router1]
				for timerange in timerange_list:
					if time_start > timerange[0] and time_end < timerange[1]:
						return True
		return False

	def getLinks(self, router, timestamp):
            temp_link_list = {}
            if router in self.link_list:
                for item in self.link_list[router]:
                    hasLink = False
                    for timerange in self.link_list[router][item]:
                        if timestamp > timerange[0] and timestamp < timerange[1]:
                            if hasLink:
                                temp_link_list[item].append(timerange)
                            else:
                                temp_link_list[item] = [timerange]
            return temp_link_list

	def getLinks2(self, router):
            temp_link_list = {}
            if router in self.link_list:
                for item in self.link_list[router]:
                    hasLink = False
                    for timerange in self.link_list[router][item]:
                        if hasLink:
                            temp_link_list[item].append(timerange)
                        else:
                            temp_link_list[item] = [timerange]
            return temp_link_list
