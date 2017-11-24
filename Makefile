include .env

export

set-pass :
	@if [ -z $(PROXY_AUTH_PASS) ]; then \
		echo "PROXY_AUTH_PASS must be set"; exit 10; \
	fi

validate :
	docker-compose config --quiet

build : validate set-pass
	docker-compose build

push :
	docker-compose push

up : set-pass
	docker-compose up -d

down :
	docker-compose down

tail :
	docker logs -f $(CONTAINER)

shell :
	docker exec -ti $(CONTAINER) /bin/bash

reset : set-pass down up

deploy :
	docker stack deploy -c docker-compose.yml $(CONTAINER)
