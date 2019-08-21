REGISTRY   := docker.io/dfkozlov
GIT_REPO   := $$(basename -s .git `git config --get remote.origin.url`)
GIT_BRANCH := $$(if [ -n "$$BRANCH_NAME" ]; then echo "$$BRANCH_NAME"; else git rev-parse --abbrev-ref HEAD; fi)
GIT_BRANCH := $$(echo "${GIT_BRANCH}" | tr '[:upper:]' '[:lower:]')
GIT_SHA1   := $$(git rev-parse HEAD)
NAME       := ${REGISTRY}/${GIT_REPO}_${GIT_BRANCH}_server
IMG_HASHED := "${NAME}:${GIT_SHA1}"
IMG_LATEST := "${NAME}:latest"
DOCKER_CMD := docker


.PHONY: clean build test push

all: clean build test push
	@echo "$@ finished!"

clean:
	[ -d .vscode/ ] && rm -rf .vscode/ || :
	[ -d .eggs/ ] && rm -rf .eggs/ || :
	[ -d .pytest_cache/ ] && rm -rf .pytest_cache/ || :
	[ -f .coverage ] && rm -f .coverage || :
	find -name __pycache__ | xargs -r rm -r

test:
	@echo "Running tests locally..."
	pytest

build:
	${DOCKER_CMD} build --no-cache -t ${IMG_HASHED} -t ${IMG_LATEST} .

test-docker:
	@echo "Testing docker image..."
	${DOCKER_CMD} run --rm --net=host \
                -v /var/run/docker.sock:/var/run/docker.sock \
                ${NAME} \
                /bin/bash -c "apt-get update && apt-get install -y make; pip3 install -r requirements/dev.txt; make test"

push:
	${DOCKER_CMD} push ${IMG_HASHED}
	${DOCKER_CMD} push ${IMG_LATEST}
