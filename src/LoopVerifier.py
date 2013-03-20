import LinkMap
import Utils
import ISISFailure
import FailureVerifier

class LoopVerifier:
    def __init__(self):
        self.util = Utils.Utils()
        self.util.ReadFormatedPingDataIntoMemory()
        self.link_map = LinkMap.LinkMap()
        self.isis_failure = ISISFailure.ISISFailure()
        self.failure_verifier = FailureVerifier.PingFailureVerifier()
        self.loop_records = self.failure_verifier.getLoops()
        self.loop_records2 = self.failure_verifier.getLoopsByRouter()

    def lookUpISISByTime(self, record):
        result = []
        for isis_record in self.isis_failure.traverse():
            if float(isis_record[4]) > record[1] + 1800:
                continue
            if float(isis_record[5]) < record[0] - 1800:
                continue
            result.append(','.join([str(r) for r in isis_record]))           
        return result

    def lookUpISISByRouter(self, record):
        result = []
        router_list = [self.failure_verifier.ipToRouter(hop.strip(), float(record[0])) for hop in record[4] if not hop == '* *']
        for isis_record in self.isis_failure.traverse():
            if isis_record[0] in router_list or isis_record[2] in router_list:
                result.append(','.join([str(r) for r in isis_record]))
        return result

    def lookUpISISByTimeAndRouter(self, record, ptime):
        result = []
        router_list = [self.failure_verifier.ipToRouter(hop.strip(), float(record[0])) for hop in record[4] if not hop == '* *']
        for isis_record in self.isis_failure.traverse():
            if float(isis_record[4]) > record[1] + 300:
                continue
            if float(isis_record[5]) < record[0] - ptime:
                continue 
            if isis_record[0] in router_list or isis_record[2] in router_list:
                result.append(','.join([str(r) for r in isis_record]))          
        return result

    def lookUpISISByCorrectPing(self, record, correct_record, ptime):
        result = []
        router_list = [self.failure_verifier.ipToRouter(hop.strip(), float(correct_record[0])) for hop in correct_record[4] if not hop == '* *']
        for isis_record in self.isis_failure.traverse():
            if float(isis_record[4]) > record[1] + 300:
                continue
            if float(isis_record[5]) < record[0] - ptime:
                continue 
            if isis_record[0] in router_list and isis_record[2] in router_list:
                result.append(','.join([str(r) for r in isis_record]))          
        return result

    def lookUpISISByRouter(self, record):
        result = []
        router_list = [self.failure_verifier.ipToRouter(hop.strip(), float(record[0])) for hop in record[4] if not hop == '* *']
        for isis_record in self.isis_failure.traverse():
            if isis_record[0] in router_list or isis_record[2] in router_list:
                result.append(','.join([str(r) for r in isis_record]))
        return result

    def lengthStatistics(self):
        for item in self.loop_records:
            print "Length: ", item, " Numbers: ", len(self.loop_records[item])
            if item > 2:
                for rec in self.loop_records[item]:
                    print item, rec

    def findsuccessLoop(self):
        count = 0
        for item in self.loop_records:
            for rec in self.loop_records[item]:
                if bool(rec[3]):
                    print rec
                    count += 1
        print count

    def findsuccessLoop2(self):
        count = 0
        for item in self.loop_records2:
            for rec in self.loop_records2[item]:
                if bool(rec[3]):
                    print item, self.failure_verifier.getPath(rec)
                    count += 1
        print count

    def loopRounds(self, record):
        hops = {}
        for hop in record[4]:
            if not hop == '* *':
                if hop in hops:
                    hops[hop] += 1
                else:
                    hops[hop] = 1
        return hops[max(hops, key = lambda x : hops[x])]


    def isIPAdjacent(self, record):
        hops = record[4]
        for i in reversed(range(len(hops))):
            if not (hops[i] == '* *' or hops[i-1] == '* *'):
                router1 = self.util.LookUp(hops[i], '', record[0]).split(',')[0]
                router2 = self.util.LookUp(hops[i-1], '', record[0]).split(',')[0]
                print router1, router2
                ip1 = [int(h) for h in hops[i].strip().split('.')]
                ip2 = [int(h) for h in hops[i-1].strip().split('.')]
                return ip1[0] == ip2[0] and ip1[1] == ip2[1] and ip1[2] == ip2[2] and abs(ip1[3] - ip2[3]) == 1
        return False

    def isRouterAdjacent(self, record):
        hops = record[4]
        for i in reversed(range(len(hops))):
            if not (hops[i] == '* *' or hops[i-1] == '* *'):
                router1 = self.util.LookUp(hops[i], '', record[0]).split(',')[0].split('-')[0]
                router2 = self.util.LookUp(hops[i-1], '', record[0]).split(',')[0].split('-')[0]
                return router1 == router2
        return False

    def adjacencyStatistics(self):
        rt_count = 0
        ip_count = 0
        count = 0
        for item in self.loop_records:
            for rec in self.loop_records[item]:
                incre = 0
                if self.isIPAdjacent(rec):
                    ip_count += 1
                    incre = 1
                if self.isRouterAdjacent(rec):
                    rt_count += 1
                    incre = 1
                count += incre
        print ip_count, rt_count, count
        return ip_count, rt_count, count
                    
    def roundStatistics(self):
        rounds = {}
        for item in self.loop_records:
            for rec in self.loop_records[item]:
                r = self.loopRounds(rec)
                if r in rounds:
                    rounds[r].append(rec)
                else:
                    rounds[r] = [rec]
        return rounds

    def findCorrectPing(self, record):
        timestamp = float('inf')
        result = None
        for ping in self.util.FindPing('', record[2]):
            if abs(timestamp - record[0]) > abs(ping[0] - record[0]) and bool(ping[3]):
                    result = ping
                    timestamp = ping[0]
        for ping in self.util.FindPing('', record[2], KeyByDest = 1):
            if abs(timestamp - record[0]) > abs(ping[0] - record[0]) and bool(ping[3]):
                    result = ping
                    timestamp = ping[0]
        return result

    def test(self):
        loop_in_isis = 0
        loop_failure = 0
        loop_statics = {}
        count = 0
        c = 0
        with open("./LoopAnalysis/LoopRecordsByCorrectPing.out", "w") as loop:
            for length in self.loop_records:
                for record in self.loop_records[length]:
                    result = self.lookUpISISByTimeAndRouter(record, 30)
                    router_list = [self.failure_verifier.ipToRouter(hop.strip(), float(record[0])) for hop in record[4] if not hop == '* *']
                    success_ping = self.findCorrectPing(record)
                    if not success_ping == None:
                        router_list1 = [self.failure_verifier.ipToRouter(hop.strip(), float(record[0])) for hop in success_ping[4] if not hop == '* *']
                        result = self.lookUpISISByCorrectPing(record, success_ping, 600000)
                    else :
                        c += 1
                    if len(result) > 0:
                        count += 1
                        loop.write('True\r')
                    else:
                        continue
                        loop.write('False\r')
                    loop.write(','.join([str(r) for r in record]) + '\r')
                    loop.write(','.join([str(r) for r in router_list]) + '\r')
                    if not success_ping == None:
                        loop.write(','.join([str(r) for r in success_ping]) + '\r')
                        loop.write(','.join([str(r) for r in router_list1]) + '\r')
                    loop.write('    ' + '\r    '.join(result) + '\r')
        print count, c

    def test_2(self):
        loop_in_isis = 0
        loop_failure = 0
        loop_statics = {}
        count = 0
        c = 0
        with open("./LoopAnalysis/LoopRecordsByTimeAndRouter.out", "w") as loop:
            for length in self.loop_records:
                for record in self.loop_records[length]:
                    result = self.lookUpISISByTimeAndRouter(record, 30)
                    router_list = [self.failure_verifier.ipToRouter(hop.strip(), float(record[0])) for hop in record[4] if not hop == '* *']
                    success_ping = self.findCorrectPing(record)
                    if not success_ping == None:
                        router_list1 = [self.failure_verifier.ipToRouter(hop.strip(), float(record[0])) for hop in success_ping[4] if not hop == '* *']
                        result = self.lookUpISISByTimeAndRouter(record, 600)
                    else :
                        c += 1
                    if len(result) > 0:
                        count += 1
                        loop.write('True\r')
                    else:
                        continue
                        loop.write('False\r')
                    loop.write(','.join([str(r) for r in record]) + '\r')
                    loop.write(','.join([str(r) for r in router_list]) + '\r')
                    if not success_ping == None:
                        loop.write(','.join([str(r) for r in success_ping]) + '\r')
                        loop.write(','.join([str(r) for r in router_list1]) + '\r')
                    loop.write('    ' + '\r    '.join(result) + '\r')
        print count, c

p = LoopVerifier()
#p.lengthStatistics()
#rs = p.roundStatistics()
#p.adjacencyStatistics()
p.findsuccessLoop2()
#p.test()
#p.test_2()
                
                
                
                       
