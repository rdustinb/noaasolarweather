#!/bin/bash

docker --debug buildx build -t digitalkrampus/noaasolarweather --platform linux/amd64,linux/arm64 .

docker push digitalkrampus/noaasolarweather
