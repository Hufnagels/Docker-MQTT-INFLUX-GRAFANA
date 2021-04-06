#!/bin/bash

cd /Users/pisti/Library/Mobile\ Documents/com~apple~CloudDocs/Projects/smarthome/Docker-MQTT-INFLUX-GRAFANA/

if [ "$1" == "start" ]; 
then 
    docker-compose up -d --no-recreate 
elif [ "$1" == "stop" ];
then 
    docker-compose down
else
    echo "Unrecognized verb",$1
fi