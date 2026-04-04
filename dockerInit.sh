#!/usr/bin/bash
currentDir=$PWD
dir="$HOME/.local/share/signal-cli"
mkdir -p $dir
echo $dir
echo directory created if not already existing.
cd $dir
git clone https://github.com/bbernhard/signal-cli-rest-api
cd signal-cli-rest-api
sudo docker build .
cd $currentDir
cp -n config.example.yaml config.yaml