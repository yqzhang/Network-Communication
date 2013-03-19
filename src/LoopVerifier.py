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

    def lookUpISISByTimeAndRouter(self, record):
        result = []
        router_list = [self.failure_verifier.ipToRouter(hop.strip(), float(record[0])) for hop in record[4] if not hop == '* *']
        print 'Router list: ', router_list
        for isis_record in self.isis_failure.traverse():
            if float(isis_record[4]) > record[1] + 3600:
                continue
            if float(isis_record[5]) < record[0] - 3600:
                continue 
            if isis_record[0] in router_list or isis_record[2] in router_list:
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

    def loopRounds(self, record):
        hops = {}
        for hop in record[4]:
            if not hop == '* *':
                if hop in hops:
                    hops[hop] += 1
                else:
                    hops[hop] = 1
        return hops[max(hops, key = lambda x : hops[x])]


            
                    
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
        with open("./LoopAnalysis/LoopRecords.out", "w") as loop:
            for length in self.loop_records:
                for record in self.loop_records[length]:
                    result = self.lookUpISISByTimeAndRouter(record)
                    router_list = [self.failure_verifier.ipToRouter(hop.strip(), float(record[0])) for hop in record[4] if not hop == '* *']
                    success_ping = self.findCorrectPing(record)
                    if not success_ping == None:
                        router_list1 = [self.failure_verifier.ipToRouter(hop.strip(), float(record[0])) for hop in success_ping[4] if not hop == '* *']
                    else :
                        c += 1
                    if len(result) > 0:
                        count += 1
                        loop.write('True\r')
                    else:
                        loop.write('False\r')
                    loop.write(','.join([str(r) for r in record]) + '\r')
                    loop.write(','.join([str(r) for r in router_list]) + '\r')
                    if not success_ping == None:
                        loop.write(','.join([str(r) for r in success_ping]) + '\r')
                        loop.write(','.join([str(r) for r in router_list1]) + '\r')
                    loop.write('    ' + '\r    '.join(result) + '\r')
                    if count < 5:
                        print '\r  '.join(self.lookUpISISByTimeAndRouter(record))
        print count, c

p = LoopVerifier()
#p.lengthStatistics()
#rs = p.roundStatistics()

#p.findsuccessLoop()
p.test()
                
                
                
                       
