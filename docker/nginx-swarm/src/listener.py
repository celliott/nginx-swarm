#!/usr/bin/env python

import os
import requests
import logging
import options

options = options.get_options()
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def parse_events(event):
  actions = ['start', 'kill']
  try:
    if event['Action'] in actions:
      item = {
        'name': event['Actor']['Attributes']['com.docker.swarm.service.name'],
        'action': event['Action'] }
      logging.info("Service {name} has been {action}ed".format(**item))
      requests.post('http://{proxy_host}:{proxy_port}/update_config'.format(**options))
  except: pass

if __name__ == "__main__":
  for event in options['docker'].events(decode=True):
    parse_events(event)
