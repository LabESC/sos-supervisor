import argparse
import os.path
from mkaosdisplay import MkaosDisplay
import requests
import monitor
import preprocessing
from settings import BASE_PATH
from utils.log import create_log
from settings import ENDPOINT, MONITOR_FILE

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-key','-k', help='mKAOS Display - Model key')
    return parser.parse_args()


if __name__ == '__main__':

    logger = create_log('sos-supervisor', filename=os.path.join(BASE_PATH, 'supervisor.log'))
    logger.debug('Starting supervisor')
    args = parse_args()
    logger.debug('Parsing arguments')
    key = args.key
    display = MkaosDisplay(ENDPOINT, key)
    endpoint = f'{ENDPOINT}{key}&'
    logger.debug('Getting mKAOS model')
    response = requests.get(endpoint + 'cmd=getEdges')
    edges = response.json()
    response = requests.get(endpoint + 'cmd=getNodes')
    nodes = response.json()
    logger.debug('Transforming mKAOS model to graph')
    Graph = preprocessing.createGraph(nodes, edges)

    display.resetDisplay(Graph)

    stop = False
    if not os.path.exists(MONITOR_FILE):
        with open(MONITOR_FILE, 'w+') as f:
            f.write('False')

    logger.debug('Running supervisor')
    while not stop:
        monitor.nodeMonitor(Graph, display)
        with open(MONITOR_FILE, 'r') as f:
            content = f.readline().strip()
            stop = content == '1' or content == 'True'

    logger.debug('Terminating supervisor')
