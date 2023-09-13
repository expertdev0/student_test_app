from bottle import run
from models import *
from api import app
from cors_setup import *

if __name__ == '__main__':
    run(app, host='localhost', port=8080)