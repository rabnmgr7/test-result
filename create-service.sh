#!/bin/bash
echo "Removing services"
docker compose down || true
echo "Removing images"
docker image rm -f test-result-flask-app:latest || true
docker image rm -f test-result-mysql-db:latest || true
docker image rm -f test-result-nginx:latest || true
echo "Creating docker compose services"
docker compose up -d
