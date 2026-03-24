#!/usr/bin/bash
export SIGNAL_SERVICE=(yq '.signal_service' config.yaml)
export PHONE_NUMBER=(yq '.phone_number' config.yaml)
DIR=$HOME/.local/share/signal-cli
CONFIG_DIR=$HOME/.local/share/signal-cli/signal-cli-config
sudo mkdir -p $DIR
cd $DIR
sudo mkdir -p $CONFIG_DIR
docker run -p 8080:8080 \
    -v $CONFIG_DIR \
    -e 'MODE=json-rpc' bbernhard/signal-cli-rest-api:latest