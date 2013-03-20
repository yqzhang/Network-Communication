from Utils import Utils
import LinkMap

# You have to provide at least <IPtoRouterFilePath> and <PingDataPath>, if the
# ping data are already formatted, you can fill in the <FormatDataPath> so
# that the class won't need to generate those formated files. If not, pass
# the <NeedFormat> param as True, and specify a location to store the formated
# files. The actual API looks like this:
#(IPtoRouterFilePath="./Cenic_failure_data/maps/ipToRouters.txt",\
# 	NeedFormat = False,FormatedPingDataPath='./',\
# 	PingDataPath = "./Cenic_failure_data/pings/"):
# So the two params that must be fill in has default values, replace the default
# if you are not following the naming rules in the default value.
########################### !!ATTENTION: God Fu, Bro Yunqi########################
# do not try to format the original ping data again, just use the ones I sent
# you, becase the original ping data has some weird things that did not follow
# the format of the data, which can not be correctly formated.
#test = Utils(NeedFormat = True)
test = Utils()
#test = Utils(FormatedPingDataPath='../data/formatpings/')


# this next line must be done in order to execute the line after it.
test.ReadFormatedPingDataIntoMemory()
#++++++++++++++++++++++++++++++++#
#pingList = dict()
#for i in test.FindPing('',''):
	#if i[0] in pingList:
		#pingList[i[0]].append(i[1]-i[0])
	#else:
		#pingList[i[0]] = [i[1]-i[0]]
#pingItemList = []
#for i in pingList:
	#pingItemList.append((i,sum(pingList[i])/len(pingList[i])))
#pingItemList = sorted(pingItemList)
#pingStatistic = open("pingToTime.txt",'w')
#for i in pingItemList:
	#pingStatistic.write("{"+str(i[0])+","+str(i[1])+"},")
#pingStatistic.close()
#++++++++++++++++++++++++++++++++#

#++++++++++++++++++++++++++++++++#
#stat = open("congestionTest1.csv",'r')
#toPing = []
#toFailure = []
#line = stat.readline()
#line = stat.readline()
#line = stat.readline()
#while line != '':
	#s = line.split(',')
	#startT = float(s[0])
	#endT = float(s[1])
	#failures = float(s[5])
	#if s[6] != '':
		#trace = float(s[6])
		#toPing.append((startT,trace))
	#toFailure.append((startT,failures))
	#line = stat.readline()
#timeToping = open("timePing.txt",'w')
#timeTofailure = open("timeFailure.txt",'w')
#for i in sorted(toPing):
	#timeToping.write("{"+str(i[0])+","+str(i[1])+"},")
#for i in sorted(toFailure):
	#timeTofailure.write("{"+str(i[0])+","+str(i[1])+"},")
#++++++++++++++++++++++++++++++++#



timeToping.close()
timeTofailure.close()


#print test.LookUp('137.164.46.77','',1353388859)
#print test.LookUp('137.164.46.245','',1353388859)
#print test.LookUp('137.164.47.128','',1353388859)
#print test.LookUp('137.164.46.80','',1353388859)
#print test.LookUp('137.164.22.45','',1353388859)
#print test.LookUp('137.164.23.53','',1353388859)
#print test.LookUp('137.164.39.157','',1353388859)
#a = test.LookUp('137.164.1.225','',1354291245)
#b = test.LookUp('137.164.34.137','',1354291245)
#c = test.LookUp('137.164.23.53','',1354291245)
#print c
#d = test.LookUp('137.164.47.129','',1354291245)
#e = test.LookUp('137.164.39.157','',1354291245)
#l = LinkMap.LinkMap()
#t = ['137.164.23.53', '137.164.47.14', '137.164.46.245', '137.164.46.77', '137.164.46.80', '137.164.1.225', '137.164.34.137']
#t2 = ['137.164.23.53', '137.164.47.14', '137.164.46.245', '137.164.47.128', '137.164.22.45', '137.164.46.31', '137.164.32.173', '137.164.34.34']
#print "==="
#for x in t2:
	#print test.LookUp(x,'',1354291245)
#print "==="
#print e
#print test.LookUp('137.164.34.34','',1354291245)
#print l.hasLink2(a.split(',')[0],b.split(',')[0],1354291217,1354291273)
#print l.getShortestPath(c.split(',')[0],d.split(',')[0])
#print l.getShortestPath(c.split(',')[0],b.split(',')[0])
#print l.getShortestPath(c.split(',')[0],e.split(',')[0])

#print test.LookUp('137.164.34.137','','')
#print test.ReverseLookup(1355453392.0, 1355453433.0, '137.164.39.158')

# Attention!!! the test.FindPing function is a generato!
# find ip data from ucsd to ip 137.164.16.21
#for i in test.FindPing('','137.164.47.120',KeyByDest = 1):
	#print i

#find ip data from any where to 137.164.16.21
#for i in test.FindPing('','137.164.16.21'):
	#print i

# find ip data from ucsb to any where
#for i in test.FindPing('ucsb',''):
	#print i

# find ip data from anywhere to anywhere
#for i in test.FindPing('',''):
	#print i

#print test.LookUp('137.164.16.1','lax-dc2,Loopback1','')
#print test.LookUp('137.164.16.21','',1351875873)
#print test.LookUp('137.164.47.159','',1351875915)
#print test.LookUp('137.164.16.46', '', 1351869317.0)
#print test.LookUp('','lax-ts-1-mgmt,FastEthernet0/0.10',253402300798)
#testip = test.LookUp('','sa-cc-1,GigabitEthernet0/1',1353318771.0)
#print testip
#print test.LookUpIP(testip)

#for i in test.FindPing('',testip):
	#print i
