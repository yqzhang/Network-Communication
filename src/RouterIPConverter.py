class RouterIPConverter:
	def __init__(self,FilePath="./Cenic_failure_data/maps/ipToRouters.txt"):
		self.IpDict = dict()
		self.RouterPortDict = dict()
		self.TimeDict = dict()
		DataFile = open(FilePath,'r')
		line = DataFile.readline()
		line = DataFile.readline()
		count = 0
		while line != '':
			s = line[:-1].split(',')

			self.IpDict[count] = s[0]
			if s[0] not in self.IpDict:
				self.IpDict[s[0]] = [count]
			else:
				self.IpDict[s[0]].extend([count])

			tmp = s[1]+','+s[2]
			self.RouterPortDict[count] = tmp
			if tmp not in self.RouterPortDict:
				self.RouterPortDict[tmp] = [count]
			else:
				self.RouterPortDict[tmp].extend([count])
			self.TimeDict[count] = s[3]

			line = DataFile.readline()
			count += 1

		DataFile.close()

# @Params:	IP, regex: "\+\d\.\+\d\.\+\d\.\+\d"
# 			RouterPort, "<RouterName>,<Port>"
#			Time, epoch time since 1970
# @Description: Given any two in Ip, RouterPort, Time,
#				the function return the one left.
# 				TODO:may be needed in the future,
#				Given all three, check if it is legal

	def LookUp(self,IP,RouterPort,Time):
		return self.__lookup__(IP,RouterPort,Time)
		#TODO:question need to ask,future work may need
		#if IP != '' and RouterPort != '' and Time != '':
			#tmpResult = self.__lookup__(IP,RouterPort,'')

	def __lookup__(self,IP,RouterPort,Time):
		if Time == '':
			# by intersect the lines from IP and RouterPort
			# we can get the time stamps where this ip assignment
			# is valid
			IPLines = self.IpDict[IP]
			RPLines = self.RouterPortDict[RouterPort]
			resultLines = set(IPLines).intersection(RPLines)
			result = []
			for i in resultLines:
				result.append(self.TimeDict[i])

			# some duplicate data are found in the data set, this
			# is simply to make the result prettier
			return set(result)
		else:
			# process over IP and RouterPort are the same, so 
			# we just need to find out which one of them is empty
			PointerNotEmpty = self.IpDict if RouterPort == '' else self.RouterPortDict
			PointerEmpty = self.IpDict if RouterPort != '' else self.RouterPortDict
			Key = IP if RouterPort == '' else RouterPort

			# find out those tuples where the time stamp of that tuple
			# is greater than the query time 
			# TODO:Equal or not?
			keyLines = PointerNotEmpty[Key]
			keyTimePairs = dict()
			for i in keyLines:
				if int(self.TimeDict[i] ) > Time:
					keyTimePairs[self.TimeDict[i]]=i

			# find out the time stamp that is closest to the query time
			# which should be the one we are looking for
			minKey = min(keyTimePairs.keys())
			result = PointerEmpty[keyTimePairs[minKey]]
			return result
































