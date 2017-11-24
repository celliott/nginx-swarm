#!/usr/bin/env python

import os
import flask
import utils
import options
from flask import request, Response

server = flask.Flask(__name__)
options = options.get_options()

@server.route("/get_endpoints", methods=['GET'])
def get_endpoints():
  results = { "endpoints": utils.get_services(options) }
  return flask.jsonify(**results)

@server.route("/update_config", methods=['POST'])
def update_config():
  results = utils.generate_config(options)
  return flask.jsonify(**results)

@server.route("/reload_nginx", methods=['POST'])
def reload_nginx():
  results = utils.reload_nginx()
  return flask.jsonify(**results)

if __name__ == "__main__":
  utils.generate_config(options)
  server.run(host='0.0.0.0', port=options['proxy_port'])
