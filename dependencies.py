import os

import networkx as nx
from operator import itemgetter

from settings import BASE_PATH
from utils.log import create_log

LOGGER = create_log('sos-supervisor', filename=os.path.join(BASE_PATH, 'supervisor.log'))


def getMissionDependencies(G, m):
    dependencies = nx.nodes(nx.dfs_tree(G, str(m)))
    return dependencies

def getMissionCandidate(G, mission):
    cList = []
    for i in G.predecessors(str(mission)):
        if(G.nodes[i]['status'] != 'failed'):
            cList.append(i)
    return cList

def getBestConstituent(G, m, cList):
    pList = []
    for c in cList:
        pList.append([c, getConstituentPriority(G,m,c)])
    LOGGER.debug(pList)
    return min(pList, key=itemgetter(1))[0]


def getConstituentMission(G, constituent):
    missionList = []
    for i in G.successors(str(constituent)):
       missionList.append(i)
    return missionList

def getConstituentPriority(G, missionId, constituentId):
    edge_priority = nx.get_edge_attributes(G, 'priority')
    return int(edge_priority[constituentId, missionId])
