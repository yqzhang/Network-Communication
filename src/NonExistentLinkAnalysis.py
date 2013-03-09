# Author: 	Dexin Qi
# Email: 	qdxzzz@gmail.com
import FailureVerifier
import LinkMap
from Utils import Utils



def nonExistentLinkAnalysis():
	''' Do something to analysis the non-existent links.  '''
	dataFile = open("NonExistentLinks.txt",'w')
	p = FailureVerifier.PingFailureVerifier()
	count = set()
	countall = set()
	countLink = set()
	countLinkNotLast = set()
	for i in p.getNonExistentLinks():
		route = i[4]
		link = i[5][0]
		countall.add(i[2])
		countLink.add(link)
		dataFile.write(str(i)+"\n")
		for j in range(len(link)):
			if route[-(j+1)] != link[-(j+1)]:
				count.add(i[2])
				countLinkNotLast.add(link)
				print route[-(j+1)] ,link,link[-(j+1)]
				#print route,link
				break
	print "All Data"
	print len(countall)
	print countall
	print "Not last hop data"
	print len(count)
	print count
	print "Links"
	print len(countLink)
	print countLink
	print "Links not last"
	print len(countLinkNotLast)
	print countLinkNotLast
	dataFile.close()

	print "=================================================="
	test = Utils()
	test.ReadFormatedPingDataIntoMemory()
	linkmap = LinkMap.LinkMap("../data/maps/links_new_format.txt")
	for i in countLink:
#TODO: 
#1.Write code here to get the router information of the ip of link i,
# use that to look up in the link map to see if the router mentioned above
# exists, how long did they last, is it possible that they are just missed?
		

		links = linkmap.getLinks2(i)
		for j in links.items():
			print j
		print "--------------------------------------------"
	
nonExistentLinkAnalysis()
