#!/bin/bash
set -e

cd ~/autonomous-api
docker rm -f autonomous-api || true
docker build -t autonomous-api .
docker run -d --name autonomous-api \
  -p 5020:8080 \
  -e SLACK_BOT_USER_OAUTH_TOKEN=$BOT_USER_OAUTH_TOKEN \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  autonomous-api
