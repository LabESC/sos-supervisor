from router import APP
from settings import PORT

if __name__ == '__main__':
    APP.run(port=PORT, host='0.0.0.0')
