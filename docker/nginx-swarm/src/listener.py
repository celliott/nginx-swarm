#!/usr/bin/env python

import os
import docker
import utils
import logging
import options

options = options.get_options()
client = docker.from_env()
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def parse_events(event):
  actions = ['start', 'kill']
  try:
    if event['Action'] in actions:
      item = {
        'name': event['Actor']['Attributes']['com.docker.swarm.service.name'],
        'action': event['Action'] }
      logging.info("Service {name} has been {action}ed".format(**item))
      utils.generate_config(options)
  except: pass

if __name__ == "__main__":
  for event in client.events(decode=True):
    parse_events(event)
