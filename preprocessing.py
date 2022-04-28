import networkx as nx
import ipaddress
import mkaosdisplay


def createGraph(nodes, edges):
    G = nx.DiGraph()

    for i in nodes:
        if(i['type'] != 'Constituent'):
            G.add_node(str(i['id']), label=i['label'], type=i['type'], id=i['id'])
        else:
            G.add_node(str(i['id']), label=i['label'], type=i['type'], ipAddress=i['ipAddress'], responseTime=i['responseTime'], availability=i['availability'], status='ok', id=i['id'])
    for i in edges:
        if(i['type'] != 'undefined'):
            if (i['type'] == 'linkCapability'):
                G.add_edge(str(i['to']), str(i['from']), id=i['id'])
            elif (i['type'] == 'linkIndividualMission'):
                G.add_edge(str(i['from']), str(i['to']), id=i['id'], priority=i['priority'])
            else:
                    G.add_edge(str(i['from']), str(i['to']), id=i['id'])
    return G

def validateContract(G):
    contractValidity = True
    for i in G.nodes:
        if (G.nodes[i]['type'] == 'Constituent' and G.nodes[i]['ipAddress'] != 'undefined'):
            if(validateIpAddress(G.nodes[i]['ipAddress']) == False):
                mkaosdisplay.sendErrorMessage(G.nodes[i]['label'] + ': IP.is.not.valid')
                contractValidity = False
                break
        if (G.nodes[i]['availability'] != ''):
            try:
                if(validateAvailability(G.nodes[i]['availability']) == False):
                    mkaosdisplay.sendErrorMessage(G.nodes[i]['label']+': Availability.value.is.not.correct')
                    contractValidity = False
                    break
            except ValueError:
                    mkaosdisplay.sendErrorMessage(G.nodes[i]['label'] + ': Availability.value.is.not.correct')
                    contractValidity = False
                    break
    return contractValidity


def validateIpAddress(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def validateAvailability(availability):
    if(float(availability) > 0 and float(availability) <= 100):
        return True
    else:
        return False
