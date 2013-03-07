#!/usr/bin/env python
# Author: Wangfan Fu
# Email: wafu@ucsd.edu

import os
import LinkMap
import Utils
import ISISFailure

class PingFailureVerifier:
    def __init__(self):
        self.isis_path = '../data/isis_failures/isis_fails_2012-11-01--2013_02_07.txt'
        self.util = Utils.Utils()
        self.util.ReadFormatedPingDataIntoMemory()
        self.link_map = LinkMap.LinkMap("../data/maps/links_new_format.txt")
        self.isis_failure = ISISFailure.ISISFailure()

    def loopDetect(self, record):
        hops = record[4]
        path = {}
        for i in range(1, len(hops)):
            if hops[i] == '* *':
                continue
            if hops[i] in path:
##                length = i - path[hops[i]]
##                ip1 = hops[len(hops)-2]
##                ip2 = hops[len(hops)-1]
##                if ip1 == '* *' or ip2 == '* *':
##                    print record, ip1, ip2
##                    continue
##                router1 = self.util.LookUp(ip1, '', record[0])
##                router2 = self.util.LookUp(ip2, '', record[0])
##                if ip1.split('.')[0] == ip2.split('.')[0] and ip1.split('.')[1] == ip2.split('.')[1] and ip1.split('.')[2] == ip2.split('.')[2] and abs(int(ip1.split('.')[3]) - int(ip2.split('.')[3])) == 1:
##                    continue
##                if router1.split('-')[0] == router2.split('-')[0]:
##                    continue
##                print record, ip1, ip2, router1, router2
                return i - path[hops[i]]
            else:
                path[hops[i]] = i
        return 0

    def nonExistentLinkDetect(self, record):
        result = []
        hops = record[4]
        for i in range(1, len(hops) - 1):
            link = (hops[i].strip(), hops[i+1].strip())
            if link[0] == '* *' or link[1] == '* *':
                continue
            if self.util.LookUp(link[0], '', float(record[0])) == None or self.util.LookUp(link[1], '', float(record[1])) == None:
                continue
            source = self.util.LookUp(link[0], '', float(record[0])).split(',')[0].strip()
            target = self.util.LookUp(link[1], '', float(record[1])).split(',')[0].strip()
            if source.split('-')[0] == target.split('-')[0]:
                continue
            if not self.link_map.hasLink2(source, target, float(record[0]), float(record[1])):
                result.append(link)
        return result
    
    def lookUpISIS(self, record):
        ip1 = record[2]
        hops = record[4]
        ip2 = hops[len(hops) - 1].strip()
        router1 = self.util.LookUp(ip1, '', float(record[0]))
        if not ip2 == '* *':
            router2 = self.util.LookUp(ip2, '', float(record[0]))
            if "Loopback" in router2:
                router2 = router1.split(',')[0]
        if "Loopback" in router1:
            router1 = router1.split(',')[0]
        result = []
        with open(self.isis_path, "r") as f:
            for line in f:
                arr = line.strip().split(',')
                r1 = arr[0] + ',' + arr[1]
                r2 = arr[2] + ',' + arr[3]
                if not (router1 in r1 or router1 in r2):
                    if ip2 == '* *' or not (router2 in r1 or router2 in r2):
                        continue
                if float(arr[4]) > record[0] or float(arr[5]) < record[1]:
                    continue
                result.append(line)
                break            
        return result

    def lookUpISIS_1(self, record):
        ip1 = record[2]
        hops = record[4]
        ip2 = hops[len(hops) - 1].strip()
        router1 = self.util.LookUp(ip1, '', float(record[0]))
        router2 = ""
        if (not router1 == None) and "Loopback" in router1:
            router1 = router1.split(',')[0]
        if not ip2 == '* *':
            router2 = self.util.LookUp(ip2, '', float(record[0]))
            if (not router2 == None) and "Loopback" in router2:
                router2 = router2.split(',')[0]
        
        result = []
        current_end_time = 0
        with open(self.isis_path, "r") as f:
            for line in f:
                arr = line.strip().split(',')
                r1 = arr[0] + ',' + arr[1]
                r2 = arr[2] + ',' + arr[3]
                if (router1 == None) or not ((router1 in r1) or (router1 in r2)):
                    if ip2 == '* *':
                        continue
                    if (router2 == None) or not ((router2 in r1) and (router2 in r2)):
                        continue
                if float(arr[4]) > record[0] + 1800 or float(arr[5]) < record[0] - 1800:
                    continue
                if current_end_time < float(arr[5]):
                    current_end_time = float(arr[5])
                    if len(result) == 0:
                        result.append(line)
                    else:
                        result[0] = line            
        return result

    def lookUpISIS_2(self, record):
        result = []
        for isis_record in self.isis_failure.traverse():
            if float(isis_record[4]) > record[1] + 1800:
                continue
            if float(isis_record[5]) < record[0] - 1800:
                continue
##            if '??' in isis_record[1] or '??' in isis_record[3]:
##                ip_record = isis_record
##            else:
##                ip_record = [self.util.LookUp('', ','.join(isis_record[0:2]), isis_record[4]),
##                             self.util.LookUp('', ','.join(isis_record[2:4]), isis_record[4]),
##                             isis_record[4], isis_record[5]]
            result.append(','.join([str(r) for r in isis_record]))           
        return result

    def lookUpISIS_3(self, record):
        result = {}
        hops = record[4]
        tmp = {}
        loop = []
        flag =False
        ip_record = []
        for hop in hops:
            if hop in tmp:
                loop.append(hop)
                break
            else:
                tmp[hop] = 1
        for hop in hops:
            if flag:
                if not hop == loop[0]:
                    loop.append(hop)
                else:
                    break
            elif hop == loop[0]:
                flag = True
        loop_router = [self.util.LookUp(hop, '', record[0]).split(',')[0].strip() for hop in loop if (not hop == '* *') and (not self.util.LookUp(hop, '', record[0]) == None)]
        for isis_record in self.isis_failure.traverse():
            if isis_record[0].strip() in loop_router and float(isis_record[4]) <= record[0]:
                if not (isis_record[0].strip() in result and float(isis_record[4]) <= float(result[isis_record[0].strip()].split(',')[4])):
                    result[isis_record[0].strip()] = ','.join([str(r) for r in isis_record])
            if isis_record[2].strip() in loop_router and float(isis_record[4]) <= record[0]:
                if not (isis_record[2].strip() in result and float(isis_record[4]) <= float(result[isis_record[2].strip()].split(',')[4])):
                    result[isis_record[2].strip()] = ','.join([str(r) for r in isis_record])
            
        return result

    def lookUpISIS_4(self, ping, record):
        flag = min([i for i in range(min([len(ping[4]), len(record[4])])) if not ping[4][i] == record[4][i]])
        result = {}
        hops = record[4]
        if flag > 0:
            for i in range(flag):
                index = flag - i - 1
                if not "* *" == hops[index]:
                    router = self.util.LookUp(hops[index], '', record[0]).split(',')[0].strip()
                    break
        else:
            router = self.util.LookUp(ping[4][flag], '', record[0]).split(',')[0].strip()
        for isis_record in self.isis_failure.traverse():
            if isis_record[0].strip() == router and float(isis_record[4]) <= record[0]:
                if not (isis_record[0].strip() in result and float(isis_record[4]) <= float(result[isis_record[0].strip()].split(',')[4])):
                    result[isis_record[0].strip()] = ','.join([str(r) for r in isis_record])
            if isis_record[2].strip() == router and float(isis_record[4]) <= record[0]:
                if not (isis_record[2].strip() in result and float(isis_record[4]) <= float(result[isis_record[2].strip()].split(',')[4])):
                    result[isis_record[2].strip()] = ','.join([str(r) for r in isis_record])
        return result

    def findCorrectPing(self, record):
        timestamp = 0
        result = None
        for ping in self.util.FindPing('', record[2]):
            if abs(timestamp - record[0]) > abs(ping[0] - record[0]) and not "* *" == ping[4][0]:
                if len([i for i in range(min([len(ping[4]), len(record[4])])) if not ping[4][i] == record[4][i]]) > 0 and 0 == self.loopDetect(ping) and "True" == str(ping[3]):
                    result = ping
                    timestamp = ping[0]
        for ping in self.util.FindPing('', record[2], KeyByDest = 1):
            if abs(timestamp - record[0]) > abs(ping[0] - record[0]) and not "* *" == ping[4][0]:
                if len([i for i in range(min([len(ping[4]), len(record[4])])) if not ping[4][i] == record[4][i]]) > 0 and 0 == self.loopDetect(ping) and "True" == str(ping[3]):
                    result = ping
                    timestamp = ping[0]
        return result
    
    def getLoops(self):
        result = {}
        with open("../data/LoopVerification5.out", "w") as loop:
            with open("../data/LinkVerification5.out", "w") as link:
                for record in self.util.FindPing('',''):                 
                    has_loop = self.loopDetect(record)                    
                    if has_loop > 0:
                        if has_loop in result:
                            result[has_loop].append(record)
                        else:
                            result[has_loop] = [record]
        return result

    def countLoops(self):
        count = 0
        loops = self.getLoops()[2]
        for record in loops:
            hops = record[4]
            ip1 = hops[len(hops)-2]
            ip2 = hops[len(hops)-1]
            if ip1 == '* *' or ip2 == '* *':
                count += 1
                continue
            router1 = self.util.LookUp(ip1, '', record[0])
            router2 = self.util.LookUp(ip2, '', record[0])
            if ip1.split('.')[0] == ip2.split('.')[0] and ip1.split('.')[1] == ip2.split('.')[1] and ip1.split('.')[2] == ip2.split('.')[2]:# and abs(int(ip1.split('.')[3]) - int(ip2.split('.')[3])) == 1:
                continue
            if router1.split('-')[0] == router2.split('-')[0]:
                continue
            count += 1
        print count, len(loops)

    def getNonExistentLinks(self):
        result = []
        for record in self.util.FindPing('',''):
            has_nonexistent_link = self.nonExistentLinkDetect(record)
            if len(has_nonexistent_link) > 0:
                record.append(has_nonexistent_link)
                result.append(record)
        return result
    
    
    def test(self):
        loop_in_isis = 0
        loop_failure = 0
        link_in_isis = 0
        link_failure = 0
        with open("../data/LoopVerification1.out", "w") as loop:
            with open("../data/LinkVerification1.out", "w") as link:
                for record in self.util.FindPing('',''):                    
                    record_str = [str(r) for r in record]                      
                    has_loop = self.loopDetect(record)
                    has_nonexistent_link = self.nonExistentLinkDetect(record)
                    
                    if has_loop > 0:
                        result = self.lookUpISIS_1(record)
                        loop_failure += 1
                        if len(result) > 0:
                            loop_in_isis += 1
                            #print record, has_loop, result
                            loop.write('True-' + ','.join(record_str) + '-' + ','.join(result) + '\r\n')
                        else:
                            loop.write('False-' + ','.join(record_str) + '-' + "No isis failure record found" + '\r\n')

                    if len(has_nonexistent_link) > 0:
                        result = self.lookUpISIS_1(record)
                        link_failure += 1
                        if len(result) > 0:
                            link_in_isis += 1
                            #print record, has_nonexistent_link, result
                            link.write('True-' + ','.join(record_str) + '-' + ','.join(result) + '\r\n')
                        else:
                            link.write('False-' + ','.join(record_str) + '-' + "No isis failure record found" + '\r\n')
                            print "No isis failure record found"

                            ip1 = record[2]
                            hops = record[4]
                            ip2 = hops[len(hops) - 1].strip()
                            router1 = self.util.LookUp(ip1, '', record[0])
                            router2 = ""
                            if not ip2 == '* *':
                                router2 = self.util.LookUp(ip2, '', record[0])
                            if "Loopback" in router1:
                                router1 = router1.split(',')[0]
                            if (not ip2 == '* *') and ("Loopback" in router2):
                                router2 = router2.split(',')[0]
                            print router1, router2
                            
        print loop_in_isis, loop_failure, link_in_isis, link_failure

    def test_2(self):
        loop_in_isis = 0
        loop_failure = 0
        loop_statics = {}
        with open("../data/LoopVerification5.out", "w") as loop:
            with open("../data/LinkVerification5.out", "w") as link:
                for record in self.util.FindPing('',''):
##                    print record
                    ip1 = record[2]
                    hops = record[4]
                    ip2 = hops[len(hops) - 1].strip()
                    router1 = self.util.LookUp(ip1, '', record[0])
                    router2 = ""
                    if not ip2 == '* *':
                        router2 = self.util.LookUp(ip2, '', record[0])                       
                        
                    record_str = [str(r) for r in record]                      
                    has_loop = self.loopDetect(record)
                    has_nonexistent_link = self.nonExistentLinkDetect(record)
                    
                    if has_loop > 0:
                        if has_loop in loop_statics:
                            loop_statics[has_loop] = loop_statics[has_loop] + 1
                        else:
                            loop_statics[has_loop] = 1
                        if has_loop > 5:
                            print record
                        loop_failure += 1
                        result = self.lookUpISIS_2(record)
                        ping = self.findCorrectPing(record)
                        if not ping == None:
                            result1 = self.lookUpISIS_4(ping, record)
                            if len(result1) > 0:
                                loop_in_isis += 1
                                loop.write('True\r\n')                                
                            loop.write('    Loop ping: ' + ','.join(record_str) + '\r\n')
                            loop.write('    Routers: ' + ','.join(self.ipToRouter(record)) + '\r\n')
                            loop.write('    Normal Ping: ' + ','.join([str(p) for p in ping]) + '\r\n')
                            loop.write('    Routers: ' + ','.join(self.ipToRouter(ping)) + '\r\n')
##                            loop.write('    ' + ','.join([ip1, ip2]) + '\r\n')
                            if len(result) > 0:
                                loop.write('    ISIS failure coincident:\r\n')
                                loop.write('      ' + '\r\n      '.join([r.strip() for r in result]) + '\r\n')
                            if len(result1) > 0:
                                loop.write('    ISIS failure on the router different from loop ping:\r\n')
                                for item in result1:
                                    loop.write('      ' + item + ' : ' + result1[item] + ' ' + str((record[0] - float(result1[item].split(',')[5]))/60) + ' ' + '\r\n')
                            loop.write('\r\n')
                        else:
                            print "no similar ping records"
                            loop.write('False\r\n')
                            loop.write('    ' + ','.join(record_str) + '\r\n')
                            loop.write('    ' + ','.join(self.ipToRouter(record)) + '\r\n')
##                            loop.write('    ' + ','.join([ip1, ip2]) + '\r\n')
                            loop.write('    ' + "No isis failure record found" + '\r\n\r\n')                            
        print loop_in_isis, loop_failure
        for item in loop_statics:
            print item, loop_statics[item]

    def ipToRouter(self, record):
        result = record[0:3]
##        for hop in record[4]:
##            if not '* *' in hop:
##                print hop, self.util.LookUp(hop.strip(), '', record[0]).strip()
        result.append([self.util.LookUp(hop.strip(), '', record[0]).strip() for hop in record[4] if (not '* *' in hop) and (not self.util.LookUp(hop.strip(), '', record[0]) == None) ])
        return [str(r) for r in result]

#p = PingFailureVerifier()
#print p.getNonExistentLinks()
