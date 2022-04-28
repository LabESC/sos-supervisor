import os

ENDPOINT = 'https://mimamura.com/diagram_homolog/api.php?key='
BASE_PATH = os.path.abspath(os.path.dirname(__file__))
MONITOR_FILE = os.path.join(BASE_PATH, 'lock')
PORT = '7474'
SERVER_LOGFILE = os.path.join(BASE_PATH, 'server.log')
