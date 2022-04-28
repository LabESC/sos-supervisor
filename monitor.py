import observationpoints
import preprocessing
from mkaosdisplay import MkaosDisplay


def nodeMonitor(G, mkaosdisplay: MkaosDisplay):
    for i in G.nodes:
        if (G.nodes[i]['type'] == 'Constituent' and preprocessing.validateIpAddress(G.nodes[i]['ipAddress'])):
            if(observationpoints.getNodeResponseTime(G.nodes[i]['ipAddress']) >= float(G.nodes[i]['responseTime']) or observationpoints.getNodeAvailability(G.nodes[i]['ipAddress']) <= float(G.nodes[i]['availability'])):
                G.nodes[i]['status'] = 'failed'
                mkaosdisplay.setFailedConstituentBackground(G.nodes[i]['id'])
            else:
                G.nodes[i]['status'] = 'ok'
    mkaosdisplay.setDisplayStatus(G)
