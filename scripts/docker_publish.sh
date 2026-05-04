#!/usr/bin/env sh
set -eu

DOCKER_USER="${DOCKER_USER:-yourusername}"

docker build -t "$DOCKER_USER/roadsense-ai-backend:latest" ./backend
docker build -t "$DOCKER_USER/roadsense-ai-frontend:latest" ./frontend
docker push "$DOCKER_USER/roadsense-ai-backend:latest"
docker push "$DOCKER_USER/roadsense-ai-frontend:latest"
