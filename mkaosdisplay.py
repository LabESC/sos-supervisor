import networkx as nx
import dependencies
import requests
from settings import ENDPOINT


class MkaosDisplay:

    def __init__(self, endpoint, key):
        self.key = key
        self.endpoint = f'{endpoint}{key}&'

    def setConstituentLabel(self, id, label):
        requests.get(self.endpoint + 'cmd=setLabel&label=' + label + '&id=' + str(id))


    def restoreConstituentBackground(self, id):
        requests.get(self.endpoint + 'cmd=setBackground&bgcolor=darkorange&id=' + str(id))


    def sendErrorMessage(self, message):
        requests.get(self.endpoint + 'cmd=sendMessage&msg_type=error&msg=' + str(message))


    def restoreMissionBackground(self, id):
        requests.get(self.endpoint + 'cmd=setBackground&bgcolor=skyblue&id=' + str(id))


    def restoreLabels(self, G):
        for i in G.nodes:
            if(G.nodes[i]['type'] == 'Constituent' or G.nodes[i]['type'] == 'Mission'):
                requests.get(self.endpoint + 'cmd=setLabel&label=' + G.nodes[i]['label'] + '&id=' + str(G.nodes[i]['id']))


    def setFailedConstituentBackground(self, id):
        requests.get(self.endpoint + 'cmd=setBackground&bgcolor=gainsboro&id=' + str(id))


    def setDisplayStatus(self, G):
        mList = []
        cList = []

        for i in G.nodes:
            if(G.nodes[i]['type'] == 'Constituent'):
                if (G.nodes[i]['status'] == 'failed'):
                    self.setFailedConstituentBackground(G.nodes[i]['id'])
                    mList = dependencies.getConstituentMission(G, G.nodes[i]['id'])
                    for m in mList:
                        cList = dependencies.getMissionCandidate(G, m)
                        if not cList:
                            missionDependencies = dependencies.getMissionDependencies(G, m)
                            self.setFailedBackground(G, missionDependencies)
                        else:
                            id_best = dependencies.getBestConstituent(G,m,cList)
                else:
                    self.restoreConstituentBackground(G.nodes[i]['id'])


    def setFailedBackground(self, G, dependencies):
        """
        Change CS background to white if it is failed
        :param G: SoS as a Graph
        :param dependencies:
        :return:
        """
        for i in dependencies:
            if(str(G.nodes[i]['id']) == i):
                if (G.nodes[i]['type'] == 'Mission'):
                    requests.get(self.endpoint + 'cmd=setBackground&bgcolor=white&id=' + str(G.nodes[i]['id']))


    def resetDisplay(self, G):
        """
        Reset mKAOS Studio Lite display
        :param G: SoS as a Graph
        :return:
        """
        for i in G.nodes:
            if(G.nodes[i]['type'] == 'Constituent'):
                self.restoreConstituentBackground(G.nodes[i]['id'])
            elif(G.nodes[i]['type'] == 'Mission'):
                self.restoreMissionBackground(G.nodes[i]['id'])
        self.restoreLabels(G)

    @staticmethod
    def setWarningColors(id, G):
        for i in G.successors(str(id)):
            edge_id = nx.get_edge_attributes(G, 'id')
