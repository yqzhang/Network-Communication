from RouterIPConverter import RouterIPConverter

test = RouterIPConverter()
#print test.LookUp('137.164.16.1','lax-dc2,Loopback1','')
print test.LookUp('137.164.40.49','',1229050280)
print test.LookUp('','lax-ts-1-mgmt,FastEthernet0/0.10',253402300798)
print test.LookUpIP('137.164.25.37')

