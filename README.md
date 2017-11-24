# nginx-swarm

A container that queries docker and generates the nginx config based on the results. nginx-swarm listens for local docker events and triggers update_config on `start` and `kill` events. You can also trigger update_config using remote calls.

TODO
- Add support for multiple replicas. Currently only supports one per container.

### Environment setup
- Requires [Docker for Mac](https://docs.docker.com/docker-for-mac/) to be installed. Docker must be version >= 1.12
- Requires [Docker Compose](https://docs.docker.com/compose/install/) to be installed to build `nginx-swarm`
- Requires `make` to be installed. To install on your Mac, run: `xcode-select --install`
- Clone this repo, navigate to it
  - `cd nginx-swarm`

### Build container
```bash
$ make build
```

### nginx-swarm demo

#### Initiate docker swarm
```bash
$ docker swarm init
```

#### Create overlay network
```bash
$ docker network create --driver overlay overlay01
```

#### Add services to docker swarm host
NOTE: use container-label to specify nginx location `--container-label endpoint=<nginx_location>`

```bash
$ docker service create \
  --replicas 1 \
  --restart-condition any \
  --name nginx-static-0-0-1 \
  --network ingress \
  --container-label endpoint=0.0.1 \
  -p 80 \
  nginx

$ docker service create \
  --replicas 1 \
  --restart-condition any \
  --name nginx-0-0-2 \
  --network ingress \
  --container-label endpoint=0.0.2 \
  -p 80 \
  nginx
```

#### Confirm nginx is proxying properly
In a browser, go to: `http://127.0.0.1/0.0.1` and `http://127.0.0.1/0.0.2`

### nginx-swarm endpoints

#### List all registered endpoints
```bash
$ curl -u $PROXY_AUTH_USER:$PROXY_AUTH_PASS http://127.0.0.1:3000/get_endpoints
```

#### Generate config based on registered services and reload nginx
```bash
$ curl -X POST -u $PROXY_AUTH_USER:$PROXY_AUTH_PASS http://127.0.0.1:3000/update_config
```

#### Reload nginx config
```bash
$ curl -X POST -u $PROXY_AUTH_USER:$PROXY_AUTH_PASS http://127.0.0.1:3000/reload_nginx
```

### Check generated config
```bash
$ docker exec -ti <container_id> /bin/bash -c "cat /etc/nginx/sites-enabled/default.conf"
```

#### Example generated config

```bash
  ...
  ## Generated config ##

  # nginx-static-0-0-1 container
  location /0.0.1/ {
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header HOST $http_host;
    proxy_set_header X-NginX-Proxy true;
    proxy_pass http://nginx-static-0-0-1:80/;
    proxy_redirect off;
  }

  # nginx-static-0-0-2 container
  location /0.0.2/ {
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header HOST $http_host;
    proxy_set_header X-NginX-Proxy true;
    proxy_pass http://nginx-static-0-0-2:80/;
    proxy_redirect off;
  }

  ## End generated config ##
  ...
```
