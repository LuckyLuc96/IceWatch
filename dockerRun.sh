#!/usr/bin/bash
currentDir=$PWD
dir=$HOME/.local/share/signal-cli
mkdir -p $dir
cd $dir
sudo docker run -p 8080:8080 \
    -v $(pwd)/signal-cli-config:$dir \
    -e 'MODE=normal' bbernhard/signal-cli-rest-api:latest
cd $currentDir