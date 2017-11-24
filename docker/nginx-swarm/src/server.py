#!/usr/bin/env python

import os
import flask
import utils
import options
from functools import wraps
from flask import request, Response

server = flask.Flask(__name__)
options = options.get_options()

def check_auth(username, password):
  """This function is called to check if a username /
  password combination is valid.
  """
  return username == options['proxy_api_user'] and password == options['proxy_api_pass']

def authenticate():
  """Sends a 401 response that enables basic auth"""
  return Response(
    'Restricted Access. Requires Authentication.', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
      return authenticate()
    return f(*args, **kwargs)
  return decorated

@server.route("/get_endpoints", methods=['GET'])
@requires_auth
def get_endpoints():
  results = { "endpoints": utils.get_services(options) }
  return flask.jsonify(**results)

@server.route("/update_config", methods=['POST'])
@requires_auth
def update_config():
  results = utils.generate_config(options)
  return flask.jsonify(**results)

@server.route("/reload_nginx", methods=['POST'])
@requires_auth
def reload_nginx():
  results = utils.reload_nginx()
  return flask.jsonify(**results)

if __name__ == "__main__":
  utils.generate_config(options)
  server.run(host='0.0.0.0', port=options['proxy_port'])
