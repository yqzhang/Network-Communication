#!/usr/bin/env python
# Author: Wangfan Fu
# Email: wafu@ucsd.edu

import copy

class LinkMap:

    def __init__(self, link_path = "../data/maps/links_new_format.txt", weight_path = "../data/maps/link_weights.txt"):
        self.link_list = {}
        num_lines = 0
        with open(weight_path, "r") as f:
            for line in f:
                num_lines += 1
                if num_lines > 1:
                    arr = line.split(',')
                    if arr[0].strip() == arr[1].strip():
                        continue
                    self.addWeight(arr[0], arr[1], int(arr[2]))
                    self.addWeight(arr[1], arr[0], int(arr[2]))
                

        num_lines = 0
        with open(link_path, "r" ) as f:
            for line in f:
                num_lines += 1
                if num_lines > 2:
                    arr = line.split(',')
                    self.addLink(arr[0], arr[2], float(arr[4]), float(arr[5].strip()))
                    self.addLink(arr[2], arr[0], float(arr[4]), float(arr[5].strip()))

    def __del__(self):
        del self.link_list

    def addLink(self, router1, router2, time_create, time_destroy):
        val = (time_create, time_destroy)
        if router1 in self.link_list:
            if router2 in self.link_list[router1]:
                self.link_list[router1][router2]['time'].append(val)
            else:
                self.link_list[router1][router2] = {'weight': float('inf'), 'time': [val]}
        else:
            self.link_list[router1] = {router2: {'weight': float('inf'), 'time': [val]}}

    def addWeight(self, router1, router2, weight):
        if "" == router1 or "" == router2:
            pass
        elif router1 in self.link_list:
            if router2 in self.link_list[router1]:
                self.link_list[router1][router2]['weight'] = weight
            else:
                self.link_list[router1][router2] = {'weight': weight, 'time': []}
        else:
            self.link_list[router1] = {router2: {'weight': weight, 'time': []}}

    def hasLink1(self, router1, router2, timestamp):
        if router1 in self.link_list and router2 in self.link_list[router1]:
            timerange_list = self.link_list[router1][router2]['time']
            for timerange in timerange_list:
                if timestamp > timerange[0] and timestamp < timerange[1]:
                    return True
        if router2 in self.link_list and router1 in self.link_list[router2]:
            timerange_list = self.link_list[router2][router1]['time']
            for timerange in timerange_list:
                if timestamp > timerange[0] and timestamp < timerange[1]:
                    return True
        return False

    def hasLink2(self, router1, router2, time_start, time_end):
        if router1 in self.link_list and router2 in self.link_list[router1]:
            timerange_list = self.link_list[router1][router2]['time']
            for timerange in timerange_list:
                if time_start > timerange[0] and time_end < timerange[1]:
                    return True
        if router2 in self.link_list and router1 in self.link_list[router2]:
            timerange_list = self.link_list[router2][router1]['time']
            for timerange in timerange_list:
                if time_start > timerange[0] and time_end < timerange[1]:
                    return True
        return False

    def getLinks(self, router, timestamp):
        temp_link_list = {}
        if router in self.link_list:
            for item in self.link_list[router]:
                if not item in temp_link_list:
                    temp_link_list[item] = {'time': [], 'weight': float('inf')}
                if 'weight' in self.link_list[router][item]:
                    temp_link_list[item]['weight'] = self.link_list[router][item]['weight']
                if 'time' in self.link_list[router][item]:
                    for timerange in self.link_list[router][item]['time']:
                        if timestamp > timerange[0] and timestamp < timerange[1]:
                            temp_link_list[item]['time'].append(timerange)
        return temp_link_list

    def getLinks2(self, router):
        if router in self.link_list:
            return self.link_list[router]

    def getWeight(self, router1, router2):
        if router1 == None or router2 == None:
            return float('inf')
        router1 = router1.strip()
        router2 = router2.strip()
        if router1 in self.link_list and router2 in self.link_list[router1] and 'weight' in self.link_list[router1][router2]:
            return self.link_list[router1][router2]['weight']
        elif router2 in self.link_list and router1 in self.link_list[router2] and 'weight' in self.link_list[router2][router1]:
            return self.link_list[router2][router1]['weight']
        else:
            return float('inf')

    def calWeight(self, path):
        total_weight = 0
        start = False
        for i in range(len(path) - 1):
            if (not start) and (not path[i] == None) and (not path[i+1] == None):
                start = True
            if start:
                total_weight += self.getWeight(path[i], path[i+1])
        return total_weight
            

    def disableLink(self, router1, router2):
        weight = float('inf')
        if router1 in self.link_list and router2 in self.link_list[router1] and 'weight' in self.link_list[router1][router2]:
            weight = self.link_list[router1][router2]['weight']
            self.link_list[router1][router2]['weight'] = float('inf')
        if router2 in self.link_list and router1 in self.link_list[router2] and 'weight' in self.link_list[router2][router1]:
            self.link_list[router2][router1]['weight'] = float('inf')
        return weight

    def enableLink(self, router1, router2, weight):
        if router1 in self.link_list and router2 in self.link_list[router1] and 'weight' in self.link_list[router1][router2]:
            if self.link_list[router1][router2]['weight'] > weight:
                self.link_list[router1][router2]['weight'] = weight
        if router2 in self.link_list and router1 in self.link_list[router2] and 'weight' in self.link_list[router2][router1]:
            if self.link_list[router2][router1]['weight'] > weight:
                self.link_list[router2][router1]['weight'] = weight

    def disableLinkList(self, links):
        weights = []
        for l in links:
            weights.append(self.disableLink(l[0], l[1]))
        return weights

    def enableLinkList(self, links, weights):
        for i in range(len(links)):
            self.enableLink(links[i][0], links[i][1], weights[i])

    def getShortestPath(self, source, dest):
        shortest_path = {source: 0}
        rest_nodes = {}
        reachable = {}
        path = {source: [source]}
        for router in self.link_list:
            rest_nodes[router] = float('inf')
        if source in rest_nodes:
            del rest_nodes[source]
        for router in self.link_list[source]:
            reachable[router] = self.link_list[source][router]['weight']
            path[router] = [source, router]
            if router in rest_nodes:
                del rest_nodes[router]
        
        while len(reachable) > 0:
            node = min(reachable, key = lambda x : reachable[x])
            length = reachable[node]
            del reachable[node]
            shortest_path[node] = length
            if node == dest:
                return path[dest], length
            for router in self.link_list[node]:
                if router in shortest_path:
                    continue
                elif router in reachable:
                    if length + self.link_list[node][router]['weight'] < reachable[router]:
                        reachable[router] = length + self.link_list[node][router]['weight']
                        path[router] = copy.deepcopy(path[node])
                        path[router].append(router)
                else:
                    del rest_nodes[router]
                    reachable[router] = length + self.link_list[node][router]['weight']
                    path[router] = copy.deepcopy(path[node])
                    path[router].append(router)
        if dest in shortest_path:
            return True, path[dest], shortest_path[dest]
        else:
            return False, path, shortest_path
            
    def getRealtimeShortestPath(self, source, dest, time, failureList):
        linkList = []
        for fail in failureList:
            if fail[4] < time and fail[5] > time:
                temp = [fail[0], fail[2]]
                linkList.append(temp)
        weightList = self.disableLinkList(linkList)
        
        # normal shortest path
        shortest_path = {source: 0}
        rest_nodes = {}
        reachable = {}
        path = {source: [source]}
        for router in self.link_list:
            rest_nodes[router] = float('inf')
        if source in rest_nodes:
            del rest_nodes[source]
        for router in self.link_list[source]:
            reachable[router] = self.link_list[source][router]['weight']
            path[router] = [source, router]
            if router in rest_nodes:
                del rest_nodes[router]
        
        while len(reachable) > 0:
            node = min(reachable, key = lambda x : reachable[x])
            length = reachable[node]
            del reachable[node]
            shortest_path[node] = length
            if node == dest:
                break
            for router in self.link_list[node]:
                if router in shortest_path:
                    continue
                elif router in reachable:
                    if length + self.link_list[node][router]['weight'] < reachable[router]:
                        reachable[router] = length + self.link_list[node][router]['weight']
                        path[router] = copy.deepcopy(path[node])
                        path[router].append(router)
                else:
                    del rest_nodes[router]
                    reachable[router] = length + self.link_list[node][router]['weight']
                    path[router] = copy.deepcopy(path[node])
                    path[router].append(router)
        # end of normal shortest path
        self.enableLinkList(linkList, weightList)

        # return result
        if dest in shortest_path:
            return path[dest], shortest_path[dest]
        else:
            return None, float('inf')

#p = LinkMap()
##for r1 in p.link_list:
##    for r2 in p.link_list[r1]:
##        if len(p.link_list[r1][r2]['time']) == 0:
##            print 'timerange = 0', r1, r2
##        elif p.link_list[r1][r2]['weight'] == 0:
##            print 'weight = 0', r1, r2
#print p.getShortestPath('riv-agg1', 'pep-gw-1')
