from flask import Flask
from flask import request

from os import path

from kubernetes import client, config
import yaml

app = Flask(__name__)

DEPLOYMENT_NAME = "nginx-deployment"


@app.route("/")
def hello():
    return "Hello from Flask!"


@app.route('/user/<name>/', methods=['GET'])
def user_view(name):
    print(name)
    return name


@app.route('/test2', methods=['GET'])
def getUserName():
    user = request.args.get('user')
    return user

if __name__ == "__main__":
    app.run(host='0.0.0.0')
