# Author: 	Dexin Qi
# Email: 	deqi@ucsd.edu
import os
import time
import traceback

# This is the class used to format the cenic data
class Utils:
	FormatedPingDataPath = '../data/formatpings/'
	SourceIDMap = {'ucsb':0,'ucla':1,'ucsd':2,'ucdavis':3,'berkeley':4,'ucsc':5}
	ParentDir = ''

	# You have to provide at least <IPtoRouterFilePath> and <PingDataPath>, if the
	# ping data are already formatted, you can fill in the <FormatDataPath> so
	# that the class won't need to generate those formated files. If not, pass
	# the <NeedFormat> param as True, and specify a location to store the formated
	# files. 
	# And the two params that must be fill in has default values, replace the default
	# if you are not following the naming rules in the default value.
	def __init__(self,
		IPtoRouterFilePath="../data/maps/ipToRouters.txt",\
		NeedFormat = False,FormatedPingDataPath='../data/formatpings/',\
		PingDataPath = "../data/pings/"):
		if os.name == 'nt':
			currentDir = os.getcwd()
			print(currentDir)
			self.ParentDir = os.path.dirname(currentDir)
			print(os.getcwd())
			print(self.ParentDir)

		if self.ParentDir != '':
			if IPtoRouterFilePath.startswith('../'):
				IPtoRouterFilePath = self.ParentDir+IPtoRouterFilePath[2:].replace('/','\\')
			if FormatedPingDataPath.startswith('../'):
				FormatedPingDataPath = self.ParentDir+FormatedPingDataPath[2:].replace('/','\\')
			if PingDataPath.startswith('../'):
				PingDataPath = self.ParentDir+PingDataPath[2:].replace('/','\\')
			if FormatedPingDataPath.startswith('../'):
				self.FormatedPingDataPath = self.ParentDir +\
				self.FormatedPingDataPath[2:].replace('/','\\')
		self.ReadRouterIPDataIntoMemory(IPtoRouterFilePath)
		if NeedFormat:
			self.FormatPingData(PingDataPath,FormatedPingDataPath)
		else:
			self.FormatedPingDataPath = FormatedPingDataPath

	# has to be done in order to execute FindPing()
	def ReadFormatedPingDataIntoMemory(self):
		formatedFiles = os.listdir(self.FormatedPingDataPath)
		self.FormatedPingDataDict = dict()
		tmpForReverseDict = []
		for i in self.SourceIDMap.items():
			tmpForReverseDict.append([i[1],i[0]])
		for i in tmpForReverseDict:
			self.SourceIDMap[i[0]] = i[1]
			
		for i in formatedFiles:
			for j in self.SourceIDMap:
				if str(j) in i:
					self.__ReadFormatedPindDataFromOneFile__(self.SourceIDMap[j],\
							self.FormatedPingDataPath+i)
					break
		
	
	# read from formated files
	def __ReadFormatedPindDataFromOneFile__(self,sourceID,filePath):
		print("Reading from:",sourceID,filePath)
		data = open(filePath,'r')
		self.FormatedPingDataDict[sourceID] = dict()
		line = data.readline()
		while True:
			line = data.readline()
			if line == '':
				break
			line = line[:-1]
			s = line.split(':')
			#s = line.split(';')
			sfront = s[0].split(',')
			sback = s[1].split(',')
			tmpTuple = []
			tmpTuple.append(float(sfront[0]))
			tmpTuple.append(float(sfront[1]))
			#tmpTuple.append(sfront[0])
			#tmpTuple.append(sfront[1])
			tmpTuple.append(sfront[2])
			tmpTuple.append(True if sfront[3]=='True' else False)
			tmpTuple.append(sback)
			if sfront[2] in self.FormatedPingDataDict[sourceID]:
				self.FormatedPingDataDict[sourceID][sfront[2]].append(tmpTuple)
			else:
				self.FormatedPingDataDict[sourceID][sfront[2]] = [tmpTuple]
		data.close()

	# read the RouterIP file into memory
	def ReadRouterIPDataIntoMemory(self,\
			IPtoRouterFilePath="../data/maps/ipToRouters.txt"):
		if self.ParentDir != '':
			if IPtoRouterFilePath.startswith('../'):
				IPtoRouterFilePath = self.ParentDir+IPtoRouterFilePath[2:].replace('/','\\')
		# Reading ip to router data into memory
		# line number->IP and IP->line numbers
		self.IpDict = dict()
		# line number->Router,port and Router,port->line numbers
		self.RouterPortDict = dict()
		# line number -> time
		self.TimeDict = dict()

		DataFile = open(IPtoRouterFilePath,'r')
		line = DataFile.readline()
		line = DataFile.readline()
		count = 0
		while line != '':
			s = line[:-1].split(',')

			# build lookup table: line number->IP
			self.IpDict[count] = s[0]
			# build lookup table: IP->line numbers
			if s[0] not in self.IpDict:
				self.IpDict[s[0]] = [count]
			else:
				self.IpDict[s[0]].extend([count])

			# build lookup table: line number->Router,port
			tmp = s[1]+','+s[2]
			self.RouterPortDict[count] = tmp
			# build lookup table: Router,port->line numbers
			if tmp not in self.RouterPortDict:
				# check if already have the item, if not then create it.
				self.RouterPortDict[tmp] = [count]
			else:
				# if already exist, extend it with the line numbers
				self.RouterPortDict[tmp].extend([count])
			# build lookup table: line number->time
			self.TimeDict[count] = s[3]

			line = DataFile.readline()
			count += 1
		DataFile.close()
		self.IPfileReadFlag = True

	# @param PingDataPath, specify where the original ping data files are
	# @param FormatDataPath, specify where the formated data should be stored
	def	FormatPingData(self,PingDataPath="../data/pings/",\
			FormatDataPath='../data/formatpings/'):
		if self.ParentDir != '':
			if FormatDataPath.startswith('../'):
				FormatDataPath = self.ParentDir+FormatDataPath[2:].replace('/','\\')
			if PingDataPath.startswith('../'):
				PingDataPath = self.ParentDir+PingDataPath[2:].replace('/','\\')
		self.FormatedPingDataPath = FormatDataPath
		fileNames = os.listdir(PingDataPath)
		tmpFileNames = []
		for i in fileNames:
			s = i.split('_')
			tmpFileNames.append(s[0])
		tmpFileNames = set(tmpFileNames)
		for i in tmpFileNames:
			for j in fileNames:
				if j.startswith(i):
					print(i,j)
					self.__ProcessPingData__(PingDataPath+j,FormatDataPath+i)

	# Data Format:
	# <start time>,<end time>,<destination>,<fail or success>:[<hops>,..]
	def __ProcessPingData__(self,dataFilePath,outputFilePath):
		dataF = open(dataFilePath,'r')
		outputF = open(outputFilePath,'a')
		line = dataF.readline()
		while line != '':
			if line.startswith('START'):
				line = dataF.readline()
				line = dataF.readline()
				# the time cut the digits after point
				startTime = line[:19]
				try:
					startTime = time.mktime(time.strptime(startTime, '%Y-%m-%d %H:%M:%S'))
					line = dataF.readline()
					endTime = line[1:20]
					endTime = time.mktime(time.strptime(endTime, '%Y-%m-%d %H:%M:%S'))
				except ValueError:
					print( "Error: There are something in the original ping data\
							file:"+dataFilePath+" that did not follow the time format.\
							The following are 100 lines of code after that exact\
							line(included), hope this will help you locate those lines.\
							And all the process of this data file will be\
							skipped, but the rest of the files will be processed.")
					# WARNING: May be I should have set a line number counter to
					# track which line was wrong, but I'm not doing it right now
					# since I have eliminated the disordered data in the current
					# data.
					for i in range(100):
						print(line)
						line = dataF.readline()
					return 0

				# extract destination
				line = dataF.readline()
				tmps = line.split(' ')
				tmpd= tmps[3]
				destination = tmps[4][1:-2]
				# check if there is any tuple of data has different behavior
				if destination != tmpd:
					print('''Warning: the destination and the one followed in the
					round brackets are not matched, in file:'''+dataFilePath)
					print(line)

				# arrival flag
				success = False
				hopList = []
				line = dataF.readline()
				while not line.startswith('END'):
					line = line[5:]
					# this is when empty line or 
					# line with * only was encountered
					if len(line) <= 10:
						if '*' in line:
							hopList.append("* *")
					else:
						s = line.split(' ')
						tmpIP = s[1][1:-1]
						# WARNING: maybe I should use regex to check the format
						# of the IP address, but here I suppose the people who
						# use this will give the correctly formatted files.
						if self.LookUpIP(tmpIP):
							hopList.append(tmpIP)
						# * at the end implies successful arrival
						#if line.endswith('*\n'):
							#success = True
							#break
					line = dataF.readline()
				if self.LookUpIP(destination):
					if len(hopList) >= 1:
						if self.LookUpIP(hopList[-1]):
							destRouterStart = self.LookUp(destination,'',startTime)
							destRouterEnd = self.LookUp(hopList[-1],'',endTime)
							if destRouterEnd.split(',')[0] == destRouterStart.split(',')[0]:
								success = True
					# write formated data into file
					outputF.write(str(startTime)+','+str(endTime)+','\
							+destination+','+str(success)+':')
					for i in hopList[:-2]:
						outputF.write(i+',')
					# this if statement exists because there is ping localhost
					# exists in the data, and there is no way 127.0.0.1
					# can be found in LookUpIP
					if len(hopList) > 0:
						outputF.write(hopList[-1])
					outputF.write('\n')
			else:
				line = dataF.readline()
		dataF.close()
		outputF.close()

	# use either the names or id for SourceID, an IP string for DestinationIP
	# ATTENTION: this function is a generator!
	def FindPing(self,SourceID,DestinationIP):
		if SourceID != '':
			if SourceID not in self.SourceIDMap and SourceID not in\
			self.SourceIDMap.values():
				raise RuntimeError("Illegal SourceID !")

			IntID = self.SourceIDMap[SourceID] if isinstance(SourceID,int) else SourceID
			if  DestinationIP != '':
				if DestinationIP in self.FormatedPingDataDict[IntID]:
					for i in self.FormatedPingDataDict[IntID][DestinationIP]:
						yield i
				else:
					print("This Source"+str(SourceID)+" has never issued \
							trace-route to destination:"+DestinationIP+" !")
			else:
				for i in self.FormatedPingDataDict[IntID].values():
					for j in i:
						yield j
		else:
			if DestinationIP != '':
				for i in range(6):
					if DestinationIP in self.FormatedPingDataDict[i]:
						for j in self.FormatedPingDataDict[i][DestinationIP]:
							yield j
					else:
						print(self.SourceIDMap[0])
						print("This Source"+self.SourceIDMap[i]+" has never issued \
								trace-route to destination:"+DestinationIP+" !")
			else:
				for i in range(6):
					for j in self.FormatedPingDataDict[i].values():
						for k in j:
							yield k

	# @Params:	IP, regex: "\+\d\.\+\d\.\+\d\.\+\d"
	# 			RouterPort, "<RouterName>,<Port>"
	#			Time, epoch time since 1970
	# @Description: Given any two in Ip, RouterPort, Time,
	#				the function return the one left.
	# 				TODO:may be needed in the future,
	#				Given all three, check if it is legal
	def LookUp(self,IP,RouterPort,Time):
		return self.__lookup__(IP,RouterPort,Time)
		#if IP != '' and RouterPort != '' and Time != '':
			#tmpResult = self.__lookup__(IP,RouterPort,'')

	def LookUpIP(self,IP):
		if IP in self.IpDict:
			return True
		else:
			return False

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


