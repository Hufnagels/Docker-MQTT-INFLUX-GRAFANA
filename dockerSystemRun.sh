#!/bin/bash

## get current dir##
_mydir="`pwd`"
echo "My working dir: $_mydir"
#cd /home/pisti/docker/Docker-MQTT-INFLUX-GRAFANA/compose_files
cd $_mydir

## check verb and run command ##
echo "$1 -ing docker containers"

if [ "$1" == "start" ]; 
then
    #docker network create -d bridge --subnet 192.168.1.0/24 --gateway 192.168.1.1 --ip-range 192.168.1.225/29 smarthome
    docker-compose up -d --no-recreate 
elif [ "$1" == "stop" ];
then 
    docker-compose down
    docker network rm smarthome
else
    echo "Unrecognized verb",$1
fi
