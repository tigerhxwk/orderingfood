
CONTAINER=bot

all: up

build:
	DOCKER_BUILDKIT=1 docker-compose build

up: build
	docker-compose up

clean:
	docker-compose rm -f $(CONTAINER)

shell: build
	docker-compose run $(CONTAINER) bash
