import os

def getNodeResponseTime(ip):
    strs = os.popen("ping -c 1 " + ip).read()
    time = strs[strs.index("time=")+len("time="):strs.index("ms")]
    return float(time)

def getNodeAvailability(ip):
    strs = os.popen("ping -c 5 " + ip).read()
    loss = strs[strs.index("received, ")+len("received, "):strs.index("%")]
    availability = 100.0 - float(loss)
    return float(availability)
