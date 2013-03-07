# Author: 	Dexin Qi
# Email: 	qdxzzz@gmail.com
import FailureVerifier

def nonExistentLinkAnalysis():
	''' Do something to analysis the non-existent links.  '''
	#dataFile = open("NonExistentLink_NotLast.txt",'w')
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
		for j in range(len(link)):
			if route[-(j+1)] != link[-(j+1)]:
				count.add(i[2])
				countLinkNotLast.add(link)
				#dataFile.write(str(i)+"\n")
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
	#dataFile.close()
	
nonExistentLinkAnalysis()
