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
test = Utils(FormatedPingDataPath='./Cenic_failure_data/formatpings/')


# this next line must be done in order to execute the line after it.
test.ReadFormatedPingDataIntoMemory()
# The following is the id of each source. You can call
# FindPing(SourceID,DestinationIP) using both ID or name(int or string) for the
# param <SourceID>
#SourceIDMap = {'ucsb':0,'ucla':1,'ucsd':2,'ucdavis':3,'berkeley':4,'ucsc':5}
for i in test.FindPing('ucsd','137.164.16.21'):
	print i

#print test.LookUp('137.164.16.1','lax-dc2,Loopback1','')
print test.LookUp('137.164.40.49','',1229050280)
print test.LookUp('','lax-ts-1-mgmt,FastEthernet0/0.10',253402300798)
print test.LookUpIP('137.164.25.37')

