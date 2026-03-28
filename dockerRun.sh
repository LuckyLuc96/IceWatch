#!/usr/bin/bash
export SIGNAL_SERVICE=(yq '.signal_service' config.yaml)
export PHONE_NUMBER=(yq '.phone_number' config.yaml)
WORKINGDIR=$PWD
DIR=$HOME/.local/share/signal-cli
CONFIG_DIR=$PWD/signal-cli-config
sudo mkdir -p $CONFIG_DIR
cd $DIR
sudo docker run -p 8080:8080 \
    -v $CONFIG_DIR:/home/.local/share/signal-cli \
    -e 'MODE=json-rpc' bbernhard/signal-cli-rest-api:latest