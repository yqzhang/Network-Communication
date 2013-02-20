from Utils import Utils

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
test = Utils(FormatedPingDataPath='../data/formatpings/')


# this next line must be done in order to execute the line after it.
test.ReadFormatedPingDataIntoMemory()
# Attention!!! the test.FindPing function is a generato!
# find ip data from ucsd to ip 137.164.16.21
for i in test.FindPing('ucsd','137.164.16.21'):
	print i
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
print test.LookUp('137.164.16.21','',1351875873)
print test.LookUp('137.164.47.159','',1351875915)
print test.LookUp('','lax-ts-1-mgmt,FastEthernet0/0.10',253402300798)
print test.LookUpIP('137.164.25.37')

