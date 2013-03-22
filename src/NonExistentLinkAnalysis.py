# Author: 	Dexin Qi
# Email: 	qdxzzz@gmail.com
import FailureVerifier
import LinkMap
import LinkMapOld
import time
import traceback
import os
from Utils import Utils
from operator import itemgetter,attrgetter

def nonExistentLinkAnalysis(missingLinks):
	''' Do something to analyze the non-existent links.  
	Print out missinglinks with their router+port, reversed
	route info position'''
	test = Utils()
	test.ReadFormatedPingDataIntoMemory()
	linkmap = LinkMap.LinkMap("../data/maps/links_new_format.txt")
	linkmapold = LinkMapOld.LinkMap("../data/maps/links_new_format.txt")

	#rfileile = open("NonExistentLinks_NotLast.txt",'w')
	logFile = open("./MissingLinkAnalysis/LogQDX.txt",'w')
	p = FailureVerifier.PingFailureVerifier()
	count = set()
	countDest = set()
	countLink = set()
	countLinkNotLast = set()
	routeCount = dict()
	for i in missingLinks:
	#for i in p.getNonExistentLinks():
		route = i[4]
		countDest.add(i[2])
		links = i[5]
		for link in links:
			time = (float(i[0])+float(i[1]))/2
			linkroute1 = test.LookUp(link[0],'',time)
			linkroute1 = linkroute1.split(',')[0] 
			linkroute2 = test.LookUp(link[1],'',time)
			linkroute2 = linkroute2.split(',')[0] 
			#if link[0] == '137.164.46.7' and link[1] == '137.164.35.47':
				#print "Found!!!:"
				#print linkroute1,linkroute2
			#if linkroute1+":"+linkroute2 not in routeCount:
			logFile.write(linkroute1+"\t"+linkroute2+"\n")
			#s1 = linkroute1.split(',')
			#s2 = linkroute2.split(',')
			#linkInfo = linkmapold.getValidTime(s1[0],s1[1],s2[0],s2[1])
			#logFile.write(str(linkInfo)+"\n")
			#logFile.write("Time:"+str(i[0])+"\t"+str(i[1])+"\n")
			logFile.write(str(i)+"\n")
			logFile.write(link[0]+"\t"+link[1]+"\n")
			logFile.write(str(test.ReverseLookup(float(i[0]),float(i[1]),i[2]))+"\n")
			logFile.write("====================================================================\n")
			if linkroute1+":"+linkroute2 in routeCount:
				routeCount[linkroute1+":"+linkroute2] += 1
			elif linkroute2+":"+linkroute1 in routeCount:
				routeCount[linkroute2+":"+linkroute1] += 1
			else:
				routeCount[linkroute1+":"+linkroute2] = 1
			countLink.add(link)

	print "RouteCount:",routeCount
	print len(routeCount)
	#rfileile.close()
	logFile.close()

	print "=================================================="

def MissingLinkVarification():
	'''Look up every missing link by src and dest, see if route
	shift occurs'''
	# By Route Shift I mean:
	# Old Route:      A--->B--->C--->D--->E
	#                           |
	#                           V
	# New Route: A--->B--->K--->L--->E
	# Trace-route will get:
	# A--->B--->C--->L--->E
	# Since trace route is composed of a bunch of pings
	test = Utils()
	test.ReadFormatedPingDataIntoMemory()
	linkmap = LinkMap.LinkMap("../data/maps/links_new_format.txt")
	p = FailureVerifier.PingFailureVerifier()

	# missing links, <original_record,missedlinks>
	MissingLinks = p.weightFilter(p.getNonExistentLinks())
	tmp = dict()
	for i in MissingLinks:
		midTime = (i[0]+i[1])/2
		for j in i[5]:
			linkroute1 = test.LookUp(j[0],'',midTime)
			linkroute1 = linkroute1.split(',')[0] 
			linkroute2 = test.LookUp(j[1],'',midTime)
			linkroute2 = linkroute2.split(',')[0] 
			if (linkroute1,linkroute2) in tmp:
				tmp[(linkroute1,linkroute2)] += 1
			elif (linkroute2,linkroute1) in tmp:
				tmp[(linkroute2,linkroute1)] += 1
			else:
				tmp[(linkroute1,linkroute2)] = 1
	print "=====================Original========================"
	countTrue = 0
	for i in MissingLinks:
		if i[3] == True:
			countTrue += 1
	print countTrue,"of nonExLink arrived at last"
	print sorted(tmp.items(), key=itemgetter(1, 0))
	print len(MissingLinks)
	print len(tmp)
	isis =	open("../data/isis_failures/isis_fails_2012-11-01--2013_02_07.txt",'r')
	line = isis.readline()
	checkList = MissingLinks[:]
	while line != '':
		s = line.split(',')
		r1 = s[0]
		r2 = s[2]
		t1 = float(s[4])
		t2 = float(s[5])
		for i in MissingLinks:
			toTest = [t1,t2,i[0],i[1]]
			toTest = sorted(toTest)
			if toTest == [t1,t2,i[0],i[1]] or toTest == [i[0],i[1],t1,t2]:
				continue
			else:
				rPath = p.getPath(i[:-1])
				if r1 in rPath or r2 in rPath:
					if i in checkList:
						checkList.remove(i)
		line = isis.readline()
	isis.close()
	print checkList
	print len(MissingLinks)
	print len(checkList)

	os.system('pause')


	# orignial tr record
	OriginalMLs = [i[:-1] for i in MissingLinks]
	log = open('./MissingLinkAnalysis/log.txt','w')
	log2 = open('./MissingLinkAnalysis/log2.txt','w')
	count = 0
	newMissingLinks = []
	for i in MissingLinks:
		CanExplain = []
		PosLink = []
		for link in i[5]:
			PosLink.append((i[4].index(link[0]),link[0]))
			CanExplain.append(False)
			PosLink.append((i[4].index(link[1]),link[1]))
			CanExplain.append(False)
		for src in range(6):
			for j in test.FindPing(src,i[2]):
				if j in OriginalMLs:
					count+=1
					#print count
					continue
				# a links can be explained if the missing link
				# appears at the same number of hops on other 
				# reached records
				for k in range(len(CanExplain)):
					if CanExplain[k] or len(j[4]) <= PosLink[k][0]:
						continue
					# may loosen the condition
					if j[4][PosLink[k][0]] == PosLink[k][1] and j[3] == True:
					#if j[4][PosLink[k][0]] == PosLink[k][1]:
						# write done how these links are explained for manual
						# verification and debug
						log.write("Before Explain:"+str(CanExplain)+'\n')
						CanExplain[k] = True
						log.write("Explain:"+str(CanExplain)+'\n')
						log.write("Missing:"+str(i)+'\n')
						if "* *" in i[4] or None in i[4]:
							log.write("Weight: inf \n")
						else:
							log.write("Weight:"+str(linkmap.calWeight(p.getPath(i[:-1])))+"\n")
						log.write("Found:"+str(j)+'\n')
						if "* *" in j[4] or None in j[4]:
							log.write("Weight: inf \n")
						else:
							log.write("Weight:"+str(linkmap.calWeight(p.getPath(j)))+"\n\n")
				if False not in CanExplain:
					break
			if False not in CanExplain:
				break
		# write links that cannot be explained
		# into a file
		if False in CanExplain:
			newMissingLinks.append(i)
			log2.write(str(CanExplain)+'\n')
			log2.write(str(PosLink)+'\n')
			log2.write(str(i)+'\n')
	log2.close()

	# count how many distinct missing links 
	tmp = set()
	for i in newMissingLinks:
		for j in i[5]:
			tmp.add((j[0],j[1]))
	print "=====================Eliminate Explained========================"
	print tmp
	print len(newMissingLinks)
	print len(tmp)
	pingPath = "../data/pings/"
	
	# eliminate thoes links with two different respond
	# to one hop of tr record which is not realized
	# when formatting the ping data
	eliminate = []
	add = []
	print "There are :",len(newMissingLinks),"new missing links"
	for i in newMissingLinks:
		r = test.ReverseLookup(float(i[0]),float(i[1]),i[2])
		s = r[0].split("'")
		fileName = s[1]
		lineNumber = int(s[2][2:-3])
		#print fileName,lineNumber
		rfile = open(pingPath+fileName,'r')
		j = 0
		line = rfile.readline()
		j += 1
		while line != '':
			if j == lineNumber and line.startswith('START'):
				line = rfile.readline()
				j += 1
				line = rfile.readline()
				j += 1
				try:
					# the time cut the digits after point
					startTime = line[:19]
					startTime = time.mktime(time.strptime(startTime, '%Y-%m-%d %H:%M:%S'))
					line = rfile.readline()
					j += 1
					endTime = line[1:20]
					endTime = time.mktime(time.strptime(endTime, '%Y-%m-%d %H:%M:%S'))
				except ValueError:
					print( "Error: There are something in the original ping data\
							file:"+rfileilePath+" that did not follow the time format.\
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
						line = rfile.readline()
						j += 1
					return 0

				# extract destination
				line = rfile.readline()
				j += 1
				tmps = line.split(' ')
				tmpd= tmps[3]
				destination = tmps[4][1:-2]
				# check if there is any tuple of data has different behavior
				if destination != tmpd:
					print('''Warning: the destination and the one followed in the
					round brackets are not matched, in file:'''+rfileilePath)
					print(line)

				# arrival flag
				success = False
				hopList = []
				line = rfile.readline()
				j += 1
				flag10 = False
				while not line.startswith('END'):
					line = line[5:]
					# this is when empty line or 
					# line with * only was encountered
					if len(line) <= 10:
						if '*' in line:
							hopList.append("* *")
					else:
						s = line.split(' ')
						# two identical response or one
						# with a missing response
						if len(s) == 8 or len(s) == 6:
							tmpIP = s[1][1:-1]
							if test.LookUpIP(tmpIP):
								hopList.append(tmpIP)
							else:
								hopList.append("* *")
						elif len(s) == 10:
							# two different response
							flag10 = True
							newIP = s[-4][1:-1]
							if test.LookUpIP(newIP):
								hopList.append(newIP)
							else:
								hopList.append("* *")
						else:
							print "Error!",s
					line = rfile.readline()
					j += 1
				if flag10:
					record = [startTime,endTime,destination,False,hopList]
					nonExLink = p.nonExistentLinkDetect(record)
					if len(nonExLink) > 0:
						print "new non existent:",nonExLink
						print record
						if len(hopList) >= 1:
							if test.LookUpIP(hopList[-1]):
								destRouterStart = test.LookUp(destination,'',startTime)
								destRouterEnd = test.LookUp(hopList[-1],'',endTime)
								if destRouterEnd == None or destRouterStart == None:
									pass
								elif destRouterEnd.split(',')[0] == destRouterStart.split(',')[0]:
									record[3]= True
								else:
									pass
						record.append(nonExLink)
						eliminate.append(i)
						add.append(record)
					else:
						#print "eliminated:",i
						eliminate.append(i)
			else:
				line = rfile.readline()
				j +=1
		rfile.close()
	for t in eliminate:
		newMissingLinks.remove(t)
	for t in add:
		newMissingLinks.append(t)
	tmp = dict()
	for i in newMissingLinks:
		for j in i[5]:
			if (j[0],j[1]) in tmp:
				tmp[(j[0],j[1])] +=1
			else:
				tmp[(j[0],j[1])] =1
	print "=====================Eliminate Different respond========================"
	print tmp.items()
	print len(newMissingLinks)
	print len(tmp)

	#nonExistentLinkAnalysis(newMissingLinks)

	# out put all the tr history for all the missing links,
	# for manual verification 
	srcList = ['ucsb','ucla','ucsd','ucdavis','berkeley','ucsc']
	dfile = open("./MissingLinkAnalysis/deeperAnalysisy.txt",'w')
	done = []
	for t in newMissingLinks:
		r = test.ReverseLookup(float(t[0]),float(t[1]),t[2])
		src = None
		for k in srcList:
			if k in r[0]:
				src = k
		#print src
		work = (src,t[2])
		if work not in done:
			toWrite = []
			for k in test.FindPing(src,t[2]):
				k.insert(0,(k[0]+k[1])/2)
				tk = k[:]
				toWrite.append(tk)
			sortToWrite = sorted(toWrite)
			dfile.write("======================="+str(len(sortToWrite))+"=======================\n")
			dfile.write("source:"+src+" dest:"+t[2]+"\n")
			dfile.write(str(t)+"\n")
			#print len(sortToWrite)
			for l in sortToWrite:
				dfile.write(str(l)+"\n")
			done.append(work)
		else:
			dfile.write("=====================================================================\n")
			dfile.write("source:"+src+" dest:"+t[2]+"\n")
			dfile.write(str(t)+"\n")
	dfile.close()
	log.close()


#nonExistentLinkAnalysis()
#MissingLinkVarification()
