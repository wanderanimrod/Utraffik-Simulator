from multiprocessing import Process
from flask import Flask
import flask

application = Flask(__name__)
from app.simulation import run


@application.route('/')
def start():
    Process(target=run).start()
    return flask.jsonify({"response": "Simulator started"})

if __name__ == '__main__':
    application.run()