#!/usr/bin/env python

import os
import io
import logging
from functools import wraps
from jinja2 import Environment, PackageLoader
from flask import request, Response

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def get_services(options):
  services = []
  for container in options['docker'].containers():
    try:
      service = options['docker'].inspect_service(
        container['Labels']['com.docker.swarm.service.id'])
      services.append( {
        'name': service['Spec']['Name'],
        'image': service['Spec']['TaskTemplate']['ContainerSpec']['Image'],
        'endpoint': service['Spec']['TaskTemplate']['ContainerSpec']['Labels']['endpoint'],
        'target_port': service['Spec']['EndpointSpec']['Ports'][0]['TargetPort'] })
    except: pass
  return services

def generate_config(options):
  logging.info("Writing nginx config: {config_path}...".format(**options))
  try:
    template_env = Environment(loader=PackageLoader('templates', 'nginx'))
    template = template_env.get_template("{template}.j2".format(**options))
    config = template.render(options=options, services=get_services(options))
    with io.FileIO(options['config_path'], "w") as file:
      file.write(config)
    reload_nginx()
    return _response('Nginx config generated and reloaded')
  except:
    err = 'Error generating Nginx config'
    logging.error(err)
    return _response(err, 1)

def reload_nginx():
  logging.info("Reloading nginx config...")
  try:
    os.system('nginx -s reload')
    return _response('Nginx config reloaded')
  except:
    err = 'Error reloading Nginx config'
    logging.error(err)
    return _response(err, 1)

def _response(msg, error=0):
  return { "msg": msg, "error": error }
