#!/bin/bash

# First remove the formattedData folder (if it exists) otherwise it will be packaged with the docker contained and owned
# by root and can never be removed...
rm -fr src/formattedData

docker --debug buildx build -t digitalkrampus/noaasolarweather --platform linux/amd64,linux/arm64 .

docker push digitalkrampus/noaasolarweather
