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

    def lookUpISIS(self, record):
        result = []
        for isis_record in self.isis_failure.traverse():
            if float(isis_record[4]) > record[1] + 1800:
                continue
            if float(isis_record[5]) < record[0] - 1800:
                continue
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


    def test(self):
        loop_in_isis = 0
        loop_failure = 0
        loop_statics = {}
        with open("./LoopAnalysis/LoopRecords.out", "w") as loop:
            for record in self.loop_records:
                hops = record[4]
                for item in record[4]:
                    ip1 = hops[len(hops) - 1].strip()
                    if not ip1 == '* *':
                        router1 = self.util.LookUp(ip1, '', record[0])
                ip2 = record[2]
                router2 = self.util.LookUp(ip1, '', record[0])
                shorestPath = self.link_map.getShortestPath(router1, router2)
                                       
                has_loop = self.failure_verifier.loopDetect(record)
                    
                if has_loop in loop_statics:
                    loop_statics[has_loop] = loop_statics[has_loop] + 1
                else:
                    loop_statics[has_loop] = 1
                if has_loop > 5:
                    print record
                result = self.lookUpISIS_2(record)
                ping = self.findCorrectPing(record)

p = LoopVerifier()
#p.lengthStatistics()
rs = p.roundStatistics()
for item in rs:
    print item, len(rs[item])
#p.findsuccessLoop()
                
                
                
                       
