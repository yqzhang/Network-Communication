import os,time
from RouterIPConverter import RouterIPConverter

# Data Format:
# <start time>,<end time>,<destination>,<fail or success>:[<hops>,..]
def ProcessPingData(dataFilePath,outputFilePath,IpLookUp):
	dataF = open(dataFilePath,'r')
	outputF = open(outputFilePath,'a')
	line = dataF.readline()
	while line != '':
		if line.startswith('START'):
			#tmptuple = []
			line = dataF.readline()

			line = dataF.readline()
			# the time cut the digits after point
			startTime = line[:19]
			try:
				startTime = time.mktime(time.strptime(startTime, '%Y-%m-%d %H:%M:%S'))
			except ValueError:
				for i in range(100):
					print line
					line = dataF.readline()
			line = dataF.readline()
			endTime = line[1:20]
			endTime = time.mktime(time.strptime(endTime, '%Y-%m-%d %H:%M:%S'))

			# extract destination
			line = dataF.readline()
			tmps = line.split(' ')
			tmpd= tmps[3]
			destination = tmps[4][1:-2]
			# check if there is any tuple of data has different behavior
			if destination != tmpd:
				print "!!!!!"
				print line

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
					if IpLookUp.LookUpIP(tmpIP):
						hopList.append(tmpIP)
					# * at the end implies successful arrival
					if line.endswith('*\n'):
						success = True
						break
				line = dataF.readline()

			# write formated data into file
			outputF.write(str(startTime)+','+str(endTime)+','\
					+destination+','+str(success)+':')
			for i in hopList[:-2]:
				outputF.write(i+',')
			# this if exists because there is ping localhost
			# exists in the data, and there is no way 127.0.0.1
			# can be found in LookUpIP
			if len(hopList) > 0:
				outputF.write(hopList[-1])
			outputF.write('\n')
		else:
			line = dataF.readline()
	dataF.close()
	outputF.close()

PingDataPath = "./Cenic_failure_data/pings/"
fileNames = os.listdir(PingDataPath)

tmpFileNames = []
for i in fileNames:
	s = i.split('_')
	tmpFileNames.append(s[0])
tmpFileNames = set(tmpFileNames)
print tmpFileNames

IPlookUp = RouterIPConverter()


for i in tmpFileNames:
	for j in fileNames:
		if j.startswith(i):
			print i,j
			ProcessPingData('./Cenic_failure_data/pings/'+j,'./Cenic_failure_data/formatpings/'+i,IPlookUp)
