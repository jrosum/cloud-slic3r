#!/usr/bin/env bash

CONTAINER_UUID="registry-docker.synyx.coffee/slic3r-web"
DOCKER_REGISTRY_URI="registry-docker.synyx.coffee"
DOCKER_USER="$user"
DOCKER_PW="$pword"

echo "==> login to docker registry=$DOCKER_REGISTRY_URI"
docker login -u "$DOCKER_USER" -p "$DOCKER_PW" "$DOCKER_REGISTRY_URI"

echo "==> building image=$CONTAINER_UUID"
docker image build --no-cache -t "$CONTAINER_UUID" -f Dockerfile .

echo "==> pushing image to docker registry=$DOCKER_REGISTRY_URI"
docker push "$CONTAINER_UUID"

STATUS=$?
if [ "$STATUS" -ne 0 ]; then
    echo "docker push didn't work!"
    exit "$?";
fi

echo "==> deleting local image=$CONTAINER_UUID"
docker rmi "$CONTAINER_UUID"
