#!/bin/bash

cd "pe-portfolio-site-project"
echo "$PWD"

git fetch && git reset origin/main --hard

docker compose -f docker-compose.prod.yml down


docker compose -f docker-compose.prod.yml up -d --buildS
