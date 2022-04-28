import os.path
import shlex
import subprocess
from flask import Flask, jsonify, request

from settings import BASE_PATH, MONITOR_FILE

APP = Flask(__name__)
APP.config['JSON_SORT_KEYS'] = False

lockRun = False

@APP.route("/")
def root():

    return jsonify({'mensagem': 'Servidor do SoS-Supervisor'}), 200


@APP.route("/supervisor/start", methods=['GET', 'POST'])
def start_supervisor():
    key = request.args.get('key', None)
    cmd_args = f'python {os.path.join(BASE_PATH, "main.py")} -k {key}'
    process = subprocess.Popen(shlex.split(cmd_args), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if process.poll() is None:
        return '', 200
    else:
        stdout, stderr = process.communicate()
        return jsonify(dict(returnconde=process.returncode, stdout=stdout.decode(), stderr=stderr.decode())), 500

@APP.route("/supervisor/stop", methods=['GET', 'POST'])
def stop_supervisor():
    with open(MONITOR_FILE, 'w+') as f:
        f.write('True')

    return '', 200
