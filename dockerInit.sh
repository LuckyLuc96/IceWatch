#!/usr/bin/bash
currentDir=$PWD
dir="$HOME/.local/share/signal-cli"
echo $dir
cd $dir
git clone https://github.com/bbernhard/signal-cli-rest-api
cd signal-cli-rest-api
echo "We will use bbernhard's entrypoint script to install the signal-cli-rest-api"
bash entrypoint.sh
sudo docker build .
cd $currentDir