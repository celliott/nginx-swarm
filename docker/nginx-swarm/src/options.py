#!/usr/bin/env python

import os
import docker

def get_options():
    return {
        'server_name': os.getenv('PROXY_SERVICE_NAME', 'swarm01'),
        'proxy_host': os.getenv('PROXY_HOST', '127.0.0.1'),
        'proxy_port': os.getenv('PROXY_PORT', '3000'),
        'proxy_domain': os.getenv('PROXY_DOMAIN', 'example.io'),
        'proxy_api_user': os.getenv('PROXY_API_USER', 'admin'),
        'proxy_api_pass': os.getenv('PROXY_API_PASS'),
        'template': os.getenv('TEMPLATE', 'default'),
        'config_path': '/etc/nginx/conf.d/default.conf',
        'docker': docker.Client(base_url='unix://var/run/docker.sock'),
    }
