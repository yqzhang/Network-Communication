#!/usr/bin/env python
# Author: Yunqi Zhang
# Email: yqzhang@ucsd.edu

from ISISFailure import Failure
from ISISFailure import ISISFailure
from Utils import Utils
from IPtoRouter import IPRouter

# Description:
# Go through all the IS-IS failures (obtained from ISISFailure.py)
# For each failure, try to find the failure in the traceroute data
# files (obtained from ProcessPingData.py)

class FailureDetection:
    failureList = list()

    # Source ID Map for ping data
    SourceIDMap = {'ucsb':0,'ucla':1,'ucsd':2,'ucdavis':3,'berkeley':4,'ucsc':5}

    def __init__(self):
        # Initiate the failure list from ISISFailure.py
        # Format: router1, port1, router2, port2, failure_start, failure_end
        self.failureList = ISISFailure().traverse()

    def lookUpByIP(self, IP, failure_start, failure_end):
        # Look up the ping data from Utils.py
        # Search by IP address
        util = Utils()
        util.ReadFormatedPingDataIntoMemory()
        for i in range(6):
            ################################
            # What is the return value ??? #
            ################################
            for data in util.FindPing(i, IP):
                # Format:
                print(data)

        # Process the return data and find the right time

        retval = list()
        for i in range(3):
            retval.append(list())
            for j in range(6):
                retval[i].append(list())

        return retval

    def lookUpByRouter(self, router, port, failure_start, failure_end):
        # Convert router:port to IP and call lookUpByIP()
        ip_router = IPRouter()
        ip_start = ip_router.query_by_router(router, port, failure_start)
        ip_end = ip_router.query_by_router(router, port, failure_end)
        if ip_start != ip_end:
            # TODO: We need to figure it out if this happens a lot
            print("Error! IP address changed during failure.")
            return NULL
        else:
            return self.lookUpByIP(ip_start, failure_start, failure_end)

    def lookUp(self):
        # Traverse the failure list and look them up
        for fail in self.failureList:
            router1 = fail[0]
            port1 = fail[1]
            router2 = fail[2]
            port2 = fail[3]
            failure_start = fail[4]
            failure_end = fail[5]
            # Format: router1, port1, router2, port2, failure_start, failure_end
            src_ping = self.lookUpByRouter(router1, port1, failure_start, failure_end)
            dst_ping = self.lookUpByRouter(router2, port2, failure_start, failure_end)
            # Before failure
            print("Before failure:")
            # During failure
            print("During failure:")
            # After failure
            print("After failure:")

fd = FailureDetection()
fd.lookUp()
